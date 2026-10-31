from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Sequence, Tuple

try:
    from .plantuml_parser import PlantUMLParser
except ImportError:  # Allows `python evaluation_script/l0_syntax.py ...`.
    from plantuml_parser import PlantUMLParser


@dataclass
class L0Result:
    passed: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    node_count: int = 0
    edge_count: int = 0


SyntaxChecker = Callable[[str], Tuple[bool, str]]


def evaluate_l0(puml_code: str, syntax_checker: SyntaxChecker | None = None) -> L0Result:
    errors: List[str] = []
    warnings: List[str] = []

    checker = syntax_checker or check_plantuml_renderable
    renderable, render_error = checker(puml_code)
    if not renderable:
        errors.append(render_error or "PlantUML render failed")

    parsed = PlantUMLParser().parse(puml_code)
    errors.extend(parsed.parse_errors)
    if not parsed.entity_nodes:
        errors.append("no parseable architecture entities")
    if not parsed.edges:
        warnings.append("no parseable architecture edges")

    return L0Result(
        passed=not errors,
        errors=errors,
        warnings=warnings,
        node_count=len(parsed.nodes),
        edge_count=len(parsed.edges),
    )


def check_plantuml_renderable(puml_code: str) -> Tuple[bool, str]:
    command = _plantuml_command()
    if not command:
        return False, "PlantUML renderer is not configured; set PLANTUML_CMD or PLANTUML_JAR"

    timeout_seconds = float(os.environ.get("PLANTUML_TIMEOUT_SECONDS", "30"))
    with tempfile.TemporaryDirectory(prefix="ma4sa_l0_") as tmp:
        tmp_path = Path(tmp)
        source_path = tmp_path / "candidate.puml"
        output_dir = tmp_path / "rendered"
        output_dir.mkdir()
        source_path.write_text(puml_code, encoding="utf-8")

        result = _run_plantuml_render(command, source_path, output_dir, timeout_seconds)
        if result.returncode != 0:
            return False, _format_plantuml_error(result.stdout, result.stderr)
        if not list(output_dir.glob("*.svg")):
            return False, "PlantUML render failed: no SVG output was produced"

    return True, ""


def _plantuml_command() -> List[str]:
    command = os.environ.get("PLANTUML_CMD")
    if command:
        return shlex.split(command, posix=True)

    jar = os.environ.get("PLANTUML_JAR")
    if jar:
        return ["java", "-jar", jar]

    executable = shutil.which("plantuml")
    if executable:
        return [executable]

    return []


def _run_plantuml_render(
    command: List[str],
    source_path: Path,
    output_dir: Path,
    timeout_seconds: float,
) -> subprocess.CompletedProcess[str]:
    args = command + ["-charset", "UTF-8", "-tsvg", "-o", str(output_dir), str(source_path)]
    try:
        return subprocess.run(
            args,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            args=args,
            returncode=124,
            stdout=exc.stdout or "",
            stderr=(exc.stderr or "") + f"\nPlantUML render timed out after {timeout_seconds:g} seconds",
        )


def _format_plantuml_error(stdout: str, stderr: str) -> str:
    details = "\n".join(part.strip() for part in [stderr, stdout] if part and part.strip())
    if not details:
        return "PlantUML render failed"
    first_lines = "\n".join(details.splitlines()[:8])
    return f"PlantUML render failed: {first_lines}"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the MA4SA L0 PlantUML renderability check.")
    parser.add_argument("puml_path", type=Path, help="Path to a .puml/.plantuml/.wsd file.")
    args = parser.parse_args(argv)

    puml_code = args.puml_path.read_text(encoding="utf-8")
    result = evaluate_l0(puml_code)

    print(f"passed: {result.passed}")
    print(f"node_count: {result.node_count}")
    print(f"edge_count: {result.edge_count}")
    if result.errors:
        print("errors:")
        for error in result.errors:
            print(f"- {error}")
    if result.warnings:
        print("warnings:")
        for warning in result.warnings:
            print(f"- {warning}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
