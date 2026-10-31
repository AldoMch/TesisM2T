from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

INPUT_NAME = "3_modelo_validado.json"
OUTPUT_NAME = "4_codigo_final.puml"
LANGUAGES = ("JAVA", "Python")

def clean_alias(component_id: str) -> str:
    return "".join(character for character in component_id if character.isalnum())

def build_aliases(components: list[dict[str, Any]]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    used_aliases: set[str] = set()

    for component in components:
        component_id = component["id"]
        base_alias = clean_alias(component_id)
        if not base_alias:
            raise ValueError(f"El id de componente '{component_id}' no contiene caracteres alfanuméricos.")

        alias = base_alias
        suffix = 1
        while alias in used_aliases:
            alias = f"{base_alias}_{suffix}"
            suffix += 1

        aliases[component_id] = alias
        used_aliases.add(alias)

    return aliases


def clean_plantuml_text(value: Any) -> str:
    return str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\r", " ").replace("\n", " ")


def connector_label(connector: dict[str, Any]) -> str:
    for key in ("type", "protocol", "name", "description"):
        value = connector.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return "relates_to"


def generate_plantuml(model: dict[str, Any]) -> str:
    components = sorted(model["components"], key=lambda component: component["id"])
    connectors = sorted(
        model["connectors"],
        key=lambda connector: (connector["source"], connector["target"], connector_label(connector)),
    )
    aliases = build_aliases(components)

    lines = ["@startuml\n"]
    for component in components:
        name = clean_plantuml_text(component["name"])
        lines.append(f'component "{name}" as {aliases[component["id"]]}\n')

    for connector in connectors:
        source = aliases[connector["source"]]
        target = aliases[connector["target"]]
        relation_type = clean_plantuml_text(connector_label(connector))
        lines.append(f"{source} --> {target} : {relation_type}\n")

    lines.append("@enduml\n")
    return "".join(lines)


def process_project(project_dir: Path) -> str:
    output_path = project_dir / OUTPUT_NAME
    if output_path.exists():
        return "ya fue transformado; se omite"

    input_path = project_dir / INPUT_NAME
    if not input_path.exists():
        return f"no existe {INPUT_NAME}; se omite"

    try:
        model = json.loads(input_path.read_text(encoding="utf-8"))
        if not isinstance(model, dict):
            raise ValueError("El modelo validado debe ser un objeto JSON.")
        plantuml = generate_plantuml(model)
        output_path.write_text(plantuml, encoding="utf-8", newline="")
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        return f"error de transformación: {error}"

    return "transformado; se creó 4_codigo_final.puml"


def main() -> int:
    parser = argparse.ArgumentParser(description="Transforma modelos validados de fase 3 a PlantUML.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("salidas_evaluacion"),
        help="Carpeta que contiene JAVA y Python (por defecto: salidas_evaluacion).",
    )
    args = parser.parse_args()

    processed = 0
    for language in LANGUAGES:
        language_dir = args.root / language
        if not language_dir.is_dir():
            print(f"[{language}] No existe la carpeta; se omite.")
            continue
        for project_dir in sorted(path for path in language_dir.iterdir() if path.is_dir()):
            print(f"[{language}/{project_dir.name}] {process_project(project_dir)}")
            processed += 1

    print(f"Fase 4 terminada. Proyectos revisados: {processed}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
