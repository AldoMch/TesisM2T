"""Fase 5: verificación de los PlantUML generados y reporte comparativo.

Para cada proyecto E-R2A de R2ABench cruza dos fuentes:

* ``salidas_evaluacion/<Lenguaje>/<Proyecto>/``: artefactos de las fases 1-4.
* ``R2ABench/Dataset/E-R2A/<Lenguaje>/<Proyecto>/``: requisitos de entrada y
  diagrama de referencia (Ground Truth) ``AD/ad.puml``.

Escribe ``RESULTADOS_VALIDACION_17_PROYECTOS.md``. No llama a ningún LLM ni
modifica el benchmark. Si PlantUML está disponible (comando ``plantuml`` o la
variable ``PLANTUML_JAR``), genera además el SVG junto a ``4_codigo_final.puml``.

La comparación con el Ground Truth es de tamaño (conteos), no de
correspondencia semántica; para L1/L2 se usa ``R2ABench/evaluation_script``.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from collections.abc import Callable, Iterable, Mapping
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from statistics import mean, median
from typing import Any, Protocol
from zoneinfo import ZoneInfo

from fase3_validacion import find_duplicate_ids, validate_candidate

LANGUAGES = ("JAVA", "Python")
REQUIREMENTS_NAME = "req_final.jsonl"
VALIDATED_MODEL_NAME = "3_modelo_validado.json"
GENERATED_PUML_NAME = "4_codigo_final.puml"
PHASE2_ERROR_NAME = "reporte_de_errores.json"
PHASE3_ERROR_NAME = "reporte_de_errores_fase3.json"
REFERENCE_PUML_PATH = Path("AD") / "ad.puml"
REPORT_NAME = "RESULTADOS_VALIDACION_17_PROYECTOS.md"
DEFAULT_DATASET_ROOT = Path("R2ABench/Dataset/E-R2A")
DEFAULT_OUTPUT_ROOT = Path("salidas_evaluacion")
RENDER_FORMAT = "svg"
RENDER_TIMEOUT_SECONDS = 120
MAX_RENDER_WORKERS = 4

STATUS_OK = "OK"
STATUS_REJECTED_PHASE2 = "Rechazado F2"
STATUS_REJECTED_PHASE3 = "Rechazado F3"
STATUS_MISSING_MODEL = "Sin modelo validado"
STATUS_MISSING_PUML = "Sin PUML"
STATUS_INVALID_PUML = "PUML inválido"
STATUS_RENDER_FAILED = "Error de render"
STATUS_READ_ERROR = "Error de lectura"

RENDER_OK = "ok"
RENDER_FAILED = "error"
RENDER_SKIPPED = "no disponible"

REFERENCE_ELEMENT_KEYWORDS = ("rectangle", "component", "database", "package", "node", "interface")
RELATION_SOLID_DIRECTED = "-->"
RELATION_DASHED_DIRECTED = "..>"
RELATION_SOLID_UNDIRECTED = "--"
RELATION_DASHED_UNDIRECTED = ".."
RELATION_CATEGORIES = (
    RELATION_SOLID_DIRECTED,
    RELATION_DASHED_DIRECTED,
    RELATION_SOLID_UNDIRECTED,
    RELATION_DASHED_UNDIRECTED,
)

MISSING_VALUE = "—"


class ArtifactReadError(Exception):
    """Un artefacto del pipeline o del benchmark no se pudo leer o interpretar."""


# --------------------------------------------------------------------------- #
# Acceso a artefactos
# --------------------------------------------------------------------------- #
def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ArtifactReadError(f"No se pudo leer {path}: {error}") from error


def read_json(path: Path) -> Any:
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as error:
        raise ArtifactReadError(f"{path} no contiene JSON válido: {error}") from error


def count_input_requirements(requirements_text: str) -> int:
    """Cuenta las líneas no vacías de un ``req_final.jsonl`` (un requisito por línea)."""
    return sum(1 for line in requirements_text.splitlines() if line.strip())


# --------------------------------------------------------------------------- #
# (a) Verificación estructural del PlantUML generado en la fase 4
# --------------------------------------------------------------------------- #
COMPONENT_LINE = re.compile(r'^component "(?:[^"\\]|\\.)*" as (?P<alias>[A-Za-z0-9_]+)$')
CONNECTOR_LINE = re.compile(r"^(?P<source>[A-Za-z0-9_]+) --> (?P<target>[A-Za-z0-9_]+) : \S.*$")


@dataclass(frozen=True)
class PumlStructureCheck:
    errors: tuple[str, ...]
    component_count: int
    connector_count: int

    @property
    def is_valid(self) -> bool:
        return not self.errors


def find_unbalanced_delimiters(text: str) -> list[str]:
    """Detecta comillas sin cerrar por línea y llaves desbalanceadas fuera de comillas."""
    errors: list[str] = []
    brace_depth = 0
    for number, line in enumerate(text.splitlines(), start=1):
        in_quotes = False
        escaped = False
        for character in line:
            if escaped:
                escaped = False
                continue
            if character == "\\":
                escaped = True
                continue
            if character == '"':
                in_quotes = not in_quotes
                continue
            if in_quotes:
                continue
            if character == "{":
                brace_depth += 1
            elif character == "}":
                brace_depth -= 1
            if brace_depth < 0:
                errors.append(f"Línea {number}: '}}' sin '{{' de apertura.")
                brace_depth = 0
        if in_quotes:
            errors.append(f"Línea {number}: comillas sin cerrar.")
    if brace_depth > 0:
        errors.append(f"Hay {brace_depth} '{{' sin cerrar.")
    return errors


def check_generated_puml(text: str) -> PumlStructureCheck:
    """Valida la gramática exacta que produce ``fase4_m2t.py``.

    Se exige: ``@startuml`` al inicio, ``@enduml`` al final, delimitadores
    balanceados, solo líneas ``component "..." as Alias`` o
    ``Alias --> Alias : etiqueta``, alias únicos y conectores entre alias
    declarados.
    """
    lines = [(number, line.strip()) for number, line in enumerate(text.splitlines(), start=1) if line.strip()]
    if not lines:
        return PumlStructureCheck(("El archivo está vacío.",), 0, 0)

    errors: list[str] = []
    if lines[0][1] != "@startuml":
        errors.append("La primera línea no es @startuml.")
    if lines[-1][1] != "@enduml":
        errors.append("La última línea no es @enduml.")
    errors.extend(find_unbalanced_delimiters(text))

    aliases: list[str] = []
    connectors: list[tuple[int, str, str]] = []
    for number, line in lines[1:-1]:
        component_match = COMPONENT_LINE.match(line)
        if component_match:
            aliases.append(component_match["alias"])
            continue
        connector_match = CONNECTOR_LINE.match(line)
        if connector_match:
            connectors.append((number, connector_match["source"], connector_match["target"]))
            continue
        errors.append(f"Línea {number} no reconocida: {line[:60]!r}.")

    for duplicate_alias in find_duplicate_ids(aliases):
        errors.append(f"Alias de componente duplicado: '{duplicate_alias}'.")

    declared_aliases = set(aliases)
    for number, source, target in connectors:
        for endpoint in (source, target):
            if endpoint not in declared_aliases:
                errors.append(f"Línea {number}: el conector usa el alias no declarado '{endpoint}'.")

    return PumlStructureCheck(tuple(errors), len(aliases), len(connectors))


# --------------------------------------------------------------------------- #
# Renderizado opcional con PlantUML (inyectable para pruebas)
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class RenderResult:
    status: str
    detail: str = ""


class DiagramRenderer(Protocol):
    description: str

    def render(self, puml_path: Path) -> RenderResult: ...


def last_non_empty_line(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines[-1] if lines else ""


class PlantUmlRenderer:
    """Ejecuta PlantUML como proceso externo; el SVG queda junto al ``.puml``."""

    def __init__(
        self,
        command: list[str],
        description: str,
        output_format: str = RENDER_FORMAT,
        timeout_seconds: int = RENDER_TIMEOUT_SECONDS,
        runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
        file_exists: Callable[[Path], bool] = Path.exists,
    ) -> None:
        self.description = description
        self._command = command
        self._output_format = output_format
        self._timeout_seconds = timeout_seconds
        self._runner = runner
        self._file_exists = file_exists

    def render(self, puml_path: Path) -> RenderResult:
        arguments = [*self._command, "-charset", "UTF-8", f"-t{self._output_format}", str(puml_path)]
        try:
            completed = self._runner(
                arguments, capture_output=True, text=True, encoding="utf-8", errors="replace",
                timeout=self._timeout_seconds, check=False
            )
        except subprocess.TimeoutExpired:
            return RenderResult(RENDER_FAILED, f"PlantUML superó el límite de {self._timeout_seconds} s.")
        except OSError as error:
            return RenderResult(RENDER_FAILED, f"No se pudo ejecutar PlantUML: {error}")

        if completed.returncode != 0:
            detail = last_non_empty_line(completed.stderr) or last_non_empty_line(completed.stdout)
            return RenderResult(RENDER_FAILED, detail or f"PlantUML terminó con código {completed.returncode}.")

        output_path = puml_path.with_suffix(f".{self._output_format}")
        if not self._file_exists(output_path):
            return RenderResult(RENDER_FAILED, "PlantUML terminó sin generar el archivo de salida.")
        return RenderResult(RENDER_OK, output_path.name)


class UnavailableRenderer:
    description = "no disponible: solo se aplicó la validación estructural"

    def render(self, puml_path: Path) -> RenderResult:
        return RenderResult(RENDER_SKIPPED, "PlantUML no está disponible.")


def build_renderer(
    environment: Mapping[str, str],
    which: Callable[[str], str | None] = shutil.which,
    is_file: Callable[[Path], bool] = Path.is_file,
) -> DiagramRenderer:
    """Elige ``plantuml`` del PATH; si no existe, ``java -jar $PLANTUML_JAR``."""
    plantuml_command = which("plantuml")
    if plantuml_command:
        return PlantUmlRenderer([plantuml_command], f"`{plantuml_command}`")

    jar_path = environment.get("PLANTUML_JAR")
    java_command = which("java")
    if jar_path and java_command and is_file(Path(jar_path)):
        command = [java_command, "-Djava.awt.headless=true", "-jar", jar_path]
        return PlantUmlRenderer(command, f"`java -jar {jar_path}`")

    return UnavailableRenderer()


# --------------------------------------------------------------------------- #
# (b) Métricas del modelo validado en la fase 3
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class ModelMetrics:
    requirement_count: int
    component_count: int
    connector_count: int
    covered_requirement_count: int

    @property
    def coverage_percent(self) -> float:
        if self.requirement_count == 0:
            return 0.0
        return 100.0 * self.covered_requirement_count / self.requirement_count


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def extract_model_metrics(model: Any) -> ModelMetrics:
    """|R_A|, |C|, |K| y requisitos de R_A referenciados por al menos un tracesTo."""
    if not isinstance(model, dict):
        raise ArtifactReadError("El modelo validado no es un objeto JSON.")

    requirements = as_list(model.get("requirements"))
    components = as_list(model.get("components"))
    connectors = as_list(model.get("connectors"))

    requirement_ids = {
        requirement["id"]
        for requirement in requirements
        if isinstance(requirement, dict) and isinstance(requirement.get("id"), str)
    }
    traced_ids = {
        trace_id
        for component in components
        if isinstance(component, dict)
        for trace_id in as_list(component.get("tracesTo"))
        if isinstance(trace_id, str)
    }
    return ModelMetrics(
        requirement_count=len(requirement_ids),
        component_count=len(components),
        connector_count=len(connectors),
        covered_requirement_count=len(requirement_ids & traced_ids),
    )


# --------------------------------------------------------------------------- #
# (c) Conteo de elementos y relaciones del Ground Truth (AD/ad.puml)
# --------------------------------------------------------------------------- #
ELEMENT_LINE = re.compile(r"^(?P<keyword>" + "|".join(REFERENCE_ELEMENT_KEYWORDS) + r")\b", re.IGNORECASE)
_ENDPOINT = r'(?:"[^"]*"|\[[^\]]*\]|[A-Za-z0-9_]+)'
_ARROW = r"<?[-.]+(?:\[[^\]]*\])?(?:up|down|left|right|u|d|l|r)?[-.]*>?"
RELATION_LINE = re.compile(
    rf"^(?P<source>{_ENDPOINT})\s*(?P<arrow>{_ARROW})\s*(?P<target>{_ENDPOINT})\s*(?::.*)?$"
)
ARROW_STYLE = re.compile(r"\[(?P<style>[^\]]*)\]")
MULTILINE_NOTE_START = re.compile(r"^note\b", re.IGNORECASE)
NOTE_END = re.compile(r"^end\s*note$", re.IGNORECASE)
LEGEND_START = re.compile(r"^legend\b", re.IGNORECASE)
LEGEND_END = re.compile(r"^end\s*legend$", re.IGNORECASE)


@dataclass(frozen=True)
class ReferenceMetrics:
    element_counts: dict[str, int]
    relation_counts: dict[str, int]

    @property
    def total_elements(self) -> int:
        return sum(self.element_counts.values())

    @property
    def total_relations(self) -> int:
        return sum(self.relation_counts.values())


def significant_lines(text: str) -> Iterable[str]:
    """Omite comentarios (``'`` y ``/' ... '/``), notas y leyendas multilínea."""
    in_block_comment = False
    closing_block: re.Pattern[str] | None = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if in_block_comment:
            in_block_comment = "'/" not in line
            continue
        if closing_block is not None:
            if closing_block.match(line):
                closing_block = None
            continue
        if not line or line.startswith("'"):
            continue
        if line.startswith("/'"):
            in_block_comment = "'/" not in line[2:]
            continue
        if MULTILINE_NOTE_START.match(line):
            # "note ... : texto" y 'note "texto" as N' ocupan una sola línea.
            if ":" not in line and '"' not in line:
                closing_block = NOTE_END
            continue
        if LEGEND_START.match(line):
            closing_block = LEGEND_END
            continue
        yield line


def classify_arrow(arrow: str) -> str:
    style_match = ARROW_STYLE.search(arrow)
    style = style_match["style"].lower() if style_match else ""
    shape = ARROW_STYLE.sub("", arrow)
    is_dashed = "." in shape or "dashed" in style or "dotted" in style
    is_directed = ">" in shape or "<" in shape
    if is_directed:
        return RELATION_DASHED_DIRECTED if is_dashed else RELATION_SOLID_DIRECTED
    return RELATION_DASHED_UNDIRECTED if is_dashed else RELATION_SOLID_UNDIRECTED


def analyze_reference_puml(text: str) -> ReferenceMetrics:
    element_counts = dict.fromkeys(REFERENCE_ELEMENT_KEYWORDS, 0)
    relation_counts = dict.fromkeys(RELATION_CATEGORIES, 0)
    for line in significant_lines(text):
        element_match = ELEMENT_LINE.match(line)
        if element_match:
            element_counts[element_match["keyword"].lower()] += 1
            continue
        relation_match = RELATION_LINE.match(line)
        if relation_match:
            relation_counts[classify_arrow(relation_match["arrow"])] += 1
    return ReferenceMetrics(element_counts, relation_counts)


# --------------------------------------------------------------------------- #
# Ensamblado por proyecto
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class ProjectPaths:
    language: str
    name: str
    dataset_dir: Path
    output_dir: Path

    @property
    def requirements_path(self) -> Path:
        return self.dataset_dir / REQUIREMENTS_NAME

    @property
    def reference_path(self) -> Path:
        return self.dataset_dir / REFERENCE_PUML_PATH

    @property
    def model_path(self) -> Path:
        return self.output_dir / VALIDATED_MODEL_NAME

    @property
    def puml_path(self) -> Path:
        return self.output_dir / GENERATED_PUML_NAME

    @property
    def phase2_error_path(self) -> Path:
        return self.output_dir / PHASE2_ERROR_NAME

    @property
    def phase3_error_path(self) -> Path:
        return self.output_dir / PHASE3_ERROR_NAME


@dataclass
class ProjectReport:
    paths: ProjectPaths
    status: str = STATUS_OK
    issues: list[str] = field(default_factory=list)
    input_requirement_count: int | None = None
    model: ModelMetrics | None = None
    puml: PumlStructureCheck | None = None
    render: RenderResult | None = None
    reference: ReferenceMetrics | None = None


def discover_projects(dataset_root: Path, output_root: Path) -> list[ProjectPaths]:
    """El dataset es la fuente de verdad: así se reportan también salidas faltantes."""
    projects: list[ProjectPaths] = []
    for language in LANGUAGES:
        language_dir = dataset_root / language
        if not language_dir.is_dir():
            continue
        project_dirs = sorted(
            (path for path in language_dir.iterdir() if (path / REQUIREMENTS_NAME).is_file()),
            key=lambda path: path.name.lower(),
        )
        for project_dir in project_dirs:
            projects.append(ProjectPaths(language, project_dir.name, project_dir, output_root / language / project_dir.name))
    return projects


def attach_dataset_metrics(report: ProjectReport) -> None:
    paths = report.paths
    try:
        report.input_requirement_count = count_input_requirements(read_text(paths.requirements_path))
    except ArtifactReadError as error:
        report.status = STATUS_READ_ERROR
        report.issues.append(str(error))
    try:
        report.reference = analyze_reference_puml(read_text(paths.reference_path))
    except ArtifactReadError as error:
        report.status = STATUS_READ_ERROR
        report.issues.append(str(error))


def phase_error_details(error_path: Path) -> list[str]:
    try:
        error_report = read_json(error_path)
    except ArtifactReadError as error:
        return [str(error)]
    if not isinstance(error_report, dict):
        return [f"{error_path.name} no tiene el formato esperado."]
    details = error_report.get("detalles") or error_report.get("detalle_python") or error_report.get("descripcion")
    if isinstance(details, list):
        return [str(detail) for detail in details]
    return [str(details)] if details else [f"Ver {error_path.name}."]


def pipeline_rejection(paths: ProjectPaths) -> tuple[str, list[str]] | None:
    if paths.phase2_error_path.exists():
        return STATUS_REJECTED_PHASE2, phase_error_details(paths.phase2_error_path)
    if paths.phase3_error_path.exists():
        return STATUS_REJECTED_PHASE3, phase_error_details(paths.phase3_error_path)
    return None


def consistency_issues(model: ModelMetrics, puml: PumlStructureCheck) -> list[str]:
    issues: list[str] = []
    if model.component_count != puml.component_count:
        issues.append(f"El PUML declara {puml.component_count} componentes y el modelo {model.component_count}.")
    if model.connector_count != puml.connector_count:
        issues.append(f"El PUML declara {puml.connector_count} conectores y el modelo {model.connector_count}.")
    return issues


def build_project_report(paths: ProjectPaths) -> ProjectReport:
    report = ProjectReport(paths)
    attach_dataset_metrics(report)

    rejection = pipeline_rejection(paths)
    if rejection is not None:
        report.status, details = rejection
        report.issues.extend(details)
        if paths.puml_path.exists():
            report.issues.append(
                f"`{GENERATED_PUML_NAME}` existe, pero se descarta porque su modelo fue rechazado."
            )
            # Revisar también el archivo histórico sin contarlo como modelo
            # aceptado ni incluirlo en las medias de los modelos válidos.
            try:
                report.puml = check_generated_puml(read_text(paths.puml_path))
                report.issues.extend(report.puml.errors)
            except ArtifactReadError as error:
                report.issues.append(str(error))
        return report

    if not paths.model_path.exists():
        report.status = STATUS_MISSING_MODEL
        return report

    try:
        model_data = read_json(paths.model_path)
        current_errors = validate_candidate(model_data)
        if current_errors:
            report.status = STATUS_REJECTED_PHASE3
            report.issues.extend(current_errors)
            return report
        report.model = extract_model_metrics(model_data)
    except ArtifactReadError as error:
        report.status = STATUS_READ_ERROR
        report.issues.append(str(error))
        return report

    if not paths.puml_path.exists():
        report.status = STATUS_MISSING_PUML
        return report

    try:
        report.puml = check_generated_puml(read_text(paths.puml_path))
    except ArtifactReadError as error:
        report.status = STATUS_READ_ERROR
        report.issues.append(str(error))
        return report

    structural_issues = [*report.puml.errors, *consistency_issues(report.model, report.puml)]
    if structural_issues:
        report.status = STATUS_INVALID_PUML
        report.issues.extend(structural_issues)
    return report


def render_valid_diagrams(
    reports: list[ProjectReport], renderer: DiagramRenderer, max_workers: int = MAX_RENDER_WORKERS
) -> None:
    renderable = [report for report in reports if report.status == STATUS_OK and report.puml is not None]
    if not renderable:
        return
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        results = list(pool.map(lambda report: renderer.render(report.paths.puml_path), renderable))
    for report, result in zip(renderable, results):
        report.render = result
        if result.status == RENDER_FAILED:
            report.status = STATUS_RENDER_FAILED
            report.issues.append(f"PlantUML: {result.detail}")


# --------------------------------------------------------------------------- #
# Reporte Markdown
# --------------------------------------------------------------------------- #
def format_number(value: float | int | None, decimals: int = 1) -> str:
    if value is None:
        return MISSING_VALUE
    if isinstance(value, int):
        return str(value)
    return f"{value:.{decimals}f}"


def format_percent(value: float | None) -> str:
    return MISSING_VALUE if value is None else f"{value:.1f} %"


def safe_ratio(numerator: int | None, denominator: int | None) -> float | None:
    if numerator is None or not denominator:
        return None
    return numerator / denominator


def mean_or_none(values: Iterable[float | int | None]) -> float | None:
    present = [value for value in values if value is not None]
    return mean(present) if present else None


def structural_cell(report: ProjectReport) -> str:
    if report.puml is None:
        return MISSING_VALUE
    if not report.puml.is_valid or report.status == STATUS_INVALID_PUML:
        return f"❌ ({len(report.issues)})"
    return "✅ histórico" if report.model is None else "✅"


def render_cell(report: ProjectReport) -> str:
    if report.render is None:
        return MISSING_VALUE
    return {RENDER_OK: "✅", RENDER_FAILED: "❌", RENDER_SKIPPED: "n/d"}[report.render.status]


@dataclass(frozen=True)
class ProjectRow:
    """Valores numéricos de una fila; ``None`` cuando no aplican."""

    input_requirements: int | None
    requirements: int | None
    components: int | None
    connectors: int | None
    coverage: float | None
    reference_elements: int | None
    reference_relations: int | None

    @property
    def components_per_reference_element(self) -> float | None:
        return safe_ratio(self.components, self.reference_elements)

    @property
    def connectors_per_reference_relation(self) -> float | None:
        return safe_ratio(self.connectors, self.reference_relations)


def to_row(report: ProjectReport) -> ProjectRow:
    model = report.model
    reference = report.reference
    return ProjectRow(
        input_requirements=report.input_requirement_count,
        requirements=model.requirement_count if model else None,
        components=model.component_count if model else None,
        connectors=model.connector_count if model else None,
        coverage=model.coverage_percent if model else None,
        reference_elements=reference.total_elements if reference else None,
        reference_relations=reference.total_relations if reference else None,
    )


def comparison_table(reports: list[ProjectReport]) -> list[str]:
    lines = [
        "| # | Lenguaje | Proyecto | Estado | \\|R\\| entrada | \\|R_A\\| | \\|C\\| | \\|K\\| | Cobertura(R_A) "
        "| Revisión estructural | Render SVG | Nodos GT | Relaciones GT | \\|C\\|/Nodos GT | \\|K\\|/Rel. GT |",
        "|---:|---|---|---|---:|---:|---:|---:|---:|:---:|:---:|---:|---:|---:|---:|",
    ]
    rows = [to_row(report) for report in reports]
    for index, (report, row) in enumerate(zip(reports, rows), start=1):
        lines.append(
            f"| {index} | {report.paths.language} | {report.paths.name} | {report.status} "
            f"| {format_number(row.input_requirements)} | {format_number(row.requirements)} "
            f"| {format_number(row.components)} | {format_number(row.connectors)} | {format_percent(row.coverage)} "
            f"| {structural_cell(report)} | {render_cell(report)} "
            f"| {format_number(row.reference_elements)} | {format_number(row.reference_relations)} "
            f"| {format_number(row.components_per_reference_element, 2)} "
            f"| {format_number(row.connectors_per_reference_relation, 2)} |"
        )
    lines.append(
        f"| | | **Promedio** | | {format_number(mean_or_none(r.input_requirements for r in rows))} "
        f"| {format_number(mean_or_none(r.requirements for r in rows))} "
        f"| {format_number(mean_or_none(r.components for r in rows))} "
        f"| {format_number(mean_or_none(r.connectors for r in rows))} "
        f"| {format_percent(mean_or_none(r.coverage for r in rows))} | | "
        f"| {format_number(mean_or_none(r.reference_elements for r in rows))} "
        f"| {format_number(mean_or_none(r.reference_relations for r in rows))} "
        f"| {format_number(mean_or_none(r.components_per_reference_element for r in rows), 2)} "
        f"| {format_number(mean_or_none(r.connectors_per_reference_relation for r in rows), 2)} |"
    )
    return lines


def descriptive_statistics_table(reports: list[ProjectReport]) -> list[str]:
    rows = [to_row(report) for report in reports]
    metrics: list[tuple[str, list[float | int | None], int]] = [
        ("\\|R_A\\| (requisitos del modelo)", [r.requirements for r in rows], 1),
        ("\\|C\\| (componentes generados)", [r.components for r in rows], 1),
        ("\\|K\\| (conectores generados)", [r.connectors for r in rows], 1),
        ("Cobertura(R_A) %", [r.coverage for r in rows], 1),
        ("Nodos GT", [r.reference_elements for r in rows], 1),
        ("Relaciones GT", [r.reference_relations for r in rows], 1),
        ("\\|C\\| / Nodos GT", [r.components_per_reference_element for r in rows], 2),
        ("\\|K\\| / Relaciones GT", [r.connectors_per_reference_relation for r in rows], 2),
    ]
    lines = ["| Métrica | n | Media | Mediana | Mín. | Máx. |", "|---|---:|---:|---:|---:|---:|"]
    for label, values, decimals in metrics:
        present = [float(value) for value in values if value is not None]
        if not present:
            lines.append(f"| {label} | 0 | {MISSING_VALUE} | {MISSING_VALUE} | {MISSING_VALUE} | {MISSING_VALUE} |")
            continue
        lines.append(
            f"| {label} | {len(present)} | {mean(present):.{decimals}f} | {median(present):.{decimals}f} "
            f"| {min(present):.{decimals}f} | {max(present):.{decimals}f} |"
        )
    return lines


def reference_breakdown_table(reports: list[ProjectReport]) -> list[str]:
    element_headers = " | ".join(f"`{keyword}`" for keyword in REFERENCE_ELEMENT_KEYWORDS)
    relation_headers = " | ".join(f"`{category}`" for category in RELATION_CATEGORIES)
    column_count = len(REFERENCE_ELEMENT_KEYWORDS) + len(RELATION_CATEGORIES) + 2
    lines = [
        f"| Proyecto | {element_headers} | **Nodos** | {relation_headers} | **Relaciones** |",
        "|---|" + "---:|" * column_count,
    ]
    references = [(report.paths.name, report.reference) for report in reports if report.reference is not None]
    for name, reference in references:
        element_cells = " | ".join(str(reference.element_counts[keyword]) for keyword in REFERENCE_ELEMENT_KEYWORDS)
        relation_cells = " | ".join(str(reference.relation_counts[category]) for category in RELATION_CATEGORIES)
        lines.append(
            f"| {name} | {element_cells} | **{reference.total_elements}** "
            f"| {relation_cells} | **{reference.total_relations}** |"
        )
    if references:
        averages = [mean(ref.element_counts[keyword] for _, ref in references) for keyword in REFERENCE_ELEMENT_KEYWORDS]
        averages.append(mean(ref.total_elements for _, ref in references))
        averages.extend(mean(ref.relation_counts[category] for _, ref in references) for category in RELATION_CATEGORIES)
        averages.append(mean(ref.total_relations for _, ref in references))
        lines.append("| **Promedio** | " + " | ".join(f"{value:.1f}" for value in averages) + " |")
    return lines


def issues_section(reports: list[ProjectReport]) -> list[str]:
    with_issues = [report for report in reports if report.issues]
    if not with_issues:
        return ["Ningún proyecto presentó incidencias."]
    lines: list[str] = []
    for report in with_issues:
        lines.append(f"- **{report.paths.language}/{report.paths.name}** ({report.status}):")
        lines.extend(f"  - {issue}" for issue in report.issues)
    return lines


def summary_section(reports: list[ProjectReport], renderer_description: str) -> list[str]:
    total = len(reports)
    validated = sum(1 for report in reports if report.model is not None)
    structurally_valid = sum(1 for report in reports if report.puml is not None and report.puml.is_valid)
    rendered = sum(1 for report in reports if report.render is not None and report.render.status == RENDER_OK)
    fully_ok = sum(1 for report in reports if report.status == STATUS_OK)
    full_coverage = sum(1 for report in reports if report.model and report.model.coverage_percent == 100.0)
    rendered_text = f"{rendered}/{total}" if not isinstance(renderer_description, str) or "no disponible" not in renderer_description else "n/d"
    return [
        f"- Proyectos E-R2A evaluados: **{total}**",
        f"- Modelos aceptados en la fase 3 (`{VALIDATED_MODEL_NAME}`): **{validated}/{total}**",
        f"- Modelos con Cobertura(R_A) = 100 %: **{full_coverage}/{validated if validated else total}**",
        f"- Archivos PlantUML estructuralmente válidos (incluidos históricos rechazados): **{structurally_valid}/{total}**",
        f"- PlantUML renderizados a {RENDER_FORMAT.upper()}: **{rendered_text}**",
        f"- Proyectos aceptados sin incidencias en esta revisión: **{fully_ok}/{total}**",
        f"- Renderizador: {renderer_description}",
    ]


METHODOLOGY_NOTES = [
    "- **\\|R\\| entrada**: líneas de `req_final.jsonl` del dataset (requisitos que recibió el LLM).",
    "- **\\|R_A\\|**: IDs únicos de requisitos en `3_modelo_validado.json`. Debe coincidir con \\|R\\| entrada.",
    "- **\\|C\\| / \\|K\\|**: componentes y conectores del modelo validado.",
    "- **Cobertura(R_A)** = \\|{r ∈ R_A : ∃ c ∈ C, r ∈ c.tracesTo}\\| / \\|R_A\\| × 100. Es una cobertura "
    "*declarada*: no prueba que el componente satisfaga el requisito.",
    "- **Revisión estructural**: `@startuml`/`@enduml`, delimitadores balanceados, solo líneas `component` y `-->`, "
    "alias únicos, conectores entre alias declarados y mismo número de componentes/conectores que el modelo.",
    "- Esta revisión local no sustituye el L0 completo de R2ABench: sin renderizador no se acredita renderizado.",
    "- Un PUML marcado como **histórico** se revisa como archivo, pero no se acepta ni se incluye en las métricas "
    "de modelos validados si tiene un reporte de rechazo de una fase previa.",
    "- **Render SVG**: compilación real con PlantUML (`n/d` si no está instalado).",
    "- **Nodos GT**: declaraciones `" + "`, `".join(REFERENCE_ELEMENT_KEYWORDS) + "` en `AD/ad.puml`. "
    "Incluye contenedores (`package`), así que no equivale a \\|C\\|: el generador solo emite `component` planos.",
    "- **Relaciones GT**: `-->` sólida dirigida (incluye `->`, `<--`, `-down->`), `..>` punteada dirigida, "
    "`--` sólida no dirigida, `..` punteada no dirigida. Se omiten comentarios, notas y leyendas.",
    "- Los cocientes \\|C\\|/Nodos GT y \\|K\\|/Rel. GT comparan **tamaño**, no correspondencia. "
    "La correspondencia (L1) y la calidad semántica (L2) requieren `R2ABench/evaluation_script`.",
    "- Los promedios se calculan sobre los proyectos en los que la métrica existe (ver n en la tabla descriptiva).",
]


def build_markdown_report(reports: list[ProjectReport], renderer_description: str, generated_at: datetime) -> str:
    sections = [
        f"# Resultados de validación: {len(reports)} proyectos E-R2A",
        "",
        f"Generado por `fase5_reporte_validacion.py` el {generated_at:%Y-%m-%d %H:%M} (America/Lima).",
        "",
        "## Resumen",
        "",
        *summary_section(reports, renderer_description),
        "",
        "## Tabla comparativa",
        "",
        *comparison_table(reports),
        "",
        "## Estadísticas descriptivas",
        "",
        *descriptive_statistics_table(reports),
        "",
        "## Desglose del Ground Truth (`AD/ad.puml`)",
        "",
        *reference_breakdown_table(reports),
        "",
        "## Incidencias",
        "",
        *issues_section(reports),
        "",
        "## Definiciones",
        "",
        *METHODOLOGY_NOTES,
        "",
    ]
    return "\n".join(sections)


# --------------------------------------------------------------------------- #
# Punto de entrada
# --------------------------------------------------------------------------- #
def parse_arguments(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verifica los PlantUML generados y compara con el Ground Truth E-R2A.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_ROOT, help="Raíz E-R2A de R2ABench.")
    parser.add_argument("--salidas", type=Path, default=DEFAULT_OUTPUT_ROOT, help="Raíz de salidas del pipeline.")
    parser.add_argument("--reporte", type=Path, default=Path(REPORT_NAME), help="Ruta del reporte Markdown.")
    parser.add_argument("--plantuml-jar", type=Path, help="Ruta a plantuml.jar (alternativa a PLANTUML_JAR).")
    parser.add_argument("--sin-render", action="store_true", help="No invoca PlantUML; solo validación estructural.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_arguments(argv)
    environment = dict(os.environ)
    if args.plantuml_jar:
        environment["PLANTUML_JAR"] = str(args.plantuml_jar)
    renderer: DiagramRenderer = UnavailableRenderer() if args.sin_render else build_renderer(environment)

    projects = discover_projects(args.dataset, args.salidas)
    if not projects:
        print(f"No se encontraron proyectos con {REQUIREMENTS_NAME} en {args.dataset}.")
        return 1

    reports = [build_project_report(paths) for paths in projects]
    render_valid_diagrams(reports, renderer)

    args.reporte.parent.mkdir(parents=True, exist_ok=True)
    args.reporte.write_text(
        build_markdown_report(reports, renderer.description, datetime.now(ZoneInfo("America/Lima"))), encoding="utf-8"
    )

    for report in reports:
        print(f"[{report.paths.language}/{report.paths.name}] {report.status}")
    print(f"Fase 5 terminada. Renderizador: {renderer.description}. Reporte: {args.reporte}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
