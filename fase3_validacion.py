from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any


INPUT_NAME = "2_candidato_materializado.json"
VALID_NAME = "3_modelo_validado.json"
ERROR_NAME = "reporte_de_errores_fase3.json"
LANGUAGES = ("JAVA", "Python")


def validate_candidate(candidate: Any) -> list[str]:
    errors: list[str] = []

    # Regla 1: estructura principal.
    if not isinstance(candidate, dict):
        return ["El candidato debe ser un objeto JSON con requirements, components y connectors."]

    required_keys = ("requirements", "components", "connectors")
    missing_keys = [key for key in required_keys if key not in candidate]
    if missing_keys:
        errors.append("Faltan las claves principales requeridas: " + ", ".join(missing_keys) + ".")

    # Las verificaciones siguientes solo se ejecutan si las colecciones existen
    requirements = candidate.get("requirements")
    components = candidate.get("components")
    connectors = candidate.get("connectors")

    requirement_ids: set[str] = set()
    if "requirements" in candidate:
        if not isinstance(requirements, list):
            errors.append("La clave 'requirements' debe contener una lista.")
        else:
            for index, requirement in enumerate(requirements):
                if not isinstance(requirement, dict) or not isinstance(requirement.get("id"), str):
                    errors.append(f"El requisito en requirements[{index}] no tiene un id de texto válido.")
                else:
                    requirement_ids.add(requirement["id"])

    component_ids: set[str] = set()
    if "components" in candidate:
        if not isinstance(components, list):
            errors.append("La clave 'components' debe contener una lista.")
        else:
            for index, component in enumerate(components):
                if not isinstance(component, dict):
                    errors.append(f"El componente en components[{index}] debe ser un objeto.")
                    continue
                component_id = component.get("id")
                if not isinstance(component_id, str):
                    errors.append(f"El componente en components[{index}] no tiene un id de texto válido.")
                else:
                    component_ids.add(component_id)

                # Regla 2: cada traza debe apuntar a un requisito existente.
                traces = component.get("tracesTo", [])
                if not isinstance(traces, list):
                    errors.append(f"El componente '{component_id or index}' tiene tracesTo que no es una lista.")
                    continue
                for trace_id in traces:
                    if trace_id not in requirement_ids:
                        errors.append(
                            f"El componente '{component_id or index}' referencia el requisito inexistente '{trace_id}' en tracesTo."
                        )

    if "connectors" in candidate:
        if not isinstance(connectors, list):
            errors.append("La clave 'connectors' debe contener una lista.")
        else:
            # Regla 3: los dos extremos deben ser IDs de componentes existentes.
            for index, connector in enumerate(connectors):
                if not isinstance(connector, dict):
                    errors.append(f"El conector en connectors[{index}] debe ser un objeto.")
                    continue
                source = connector.get("source")
                target = connector.get("target")
                if source not in component_ids:
                    errors.append(f"El conector {index} tiene source inexistente: '{source}'.")
                if target not in component_ids:
                    errors.append(f"El conector {index} tiene target inexistente: '{target}'.")

    return errors


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def process_project(project_dir: Path) -> str:
    valid_path = project_dir / VALID_NAME
    error_path = project_dir / ERROR_NAME
    if valid_path.exists() or error_path.exists():
        return "ya fue validado; se omite"

    input_path = project_dir / INPUT_NAME
    if not input_path.exists():
        return f"no existe {INPUT_NAME}; se omite"

    try:
        candidate = json.loads(input_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        report = {
            "fase_fallo": "Fase 3 (Validación Determinista)",
            "error_tipo": "Violación de Integridad Referencial",
            "detalles": [f"No se pudo leer el candidato materializado: {error}"],
        }
        write_json(error_path, report)
        return "rechazado; el archivo JSON no se pudo leer"

    errors = validate_candidate(candidate)
    if errors:
        report = {
            "fase_fallo": "Fase 3 (Validación Determinista)",
            "error_tipo": "Violación de Integridad Referencial",
            "detalles": errors,
        }
        write_json(error_path, report)
        return f"rechazado; {len(errors)} error(es) registrado(s)"

    # Se vuelve a serializar con dos espacios, sin transformar el contenido.
    write_json(valid_path, candidate)
    return "válido; se creó 3_modelo_validado.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida candidatos materializados de la fase 2.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("salidas_evaluacion"),
        help="Carpeta que contiene JAVA y Python (por defecto: salidas_evaluacion).",
    )
    args = parser.parse_args()

    root = args.root
    processed = 0
    for language in LANGUAGES:
        language_dir = root / language
        if not language_dir.is_dir():
            print(f"[{language}] No existe la carpeta; se omite.")
            continue
        for project_dir in sorted(path for path in language_dir.iterdir() if path.is_dir()):
            print(f"[{language}/{project_dir.name}] {process_project(project_dir)}")
            processed += 1

    print(f"Fase 3 terminada. Proyectos revisados: {processed}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
