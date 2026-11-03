"""Pruebas locales de integridad y reporte; no realizan llamadas a modelos."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from fase3_validacion import process_project, validate_candidate
from fase5_reporte_validacion import (
    STATUS_REJECTED_PHASE3,
    ProjectPaths,
    analyze_reference_puml,
    build_project_report,
    check_generated_puml,
    extract_model_metrics,
)


def valid_model():
    return {
        "requirements": [{"id": "R1"}, {"id": "R2"}],
        "components": [
            {"id": "A", "name": "Servicio", "tracesTo": ["R1"]},
            {"id": "B", "name": "Almacén", "tracesTo": ["R2"]},
        ],
        "connectors": [{"source": "A", "target": "B", "type": "usa"}],
    }


VALID_PUML = '@startuml\ncomponent "Servicio" as A\ncomponent "Almacén" as B\nA --> B : usa\n@enduml\n'


class IntegrityTests(unittest.TestCase):
    def test_valid_model_and_full_declared_coverage(self):
        model = valid_model()
        self.assertEqual(validate_candidate(model), [])
        self.assertEqual(extract_model_metrics(model).coverage_percent, 100.0)

    def test_duplicate_requirement_and_component_are_both_reported(self):
        model = valid_model()
        model["requirements"].append(copy.deepcopy(model["requirements"][0]))
        model["components"].append(copy.deepcopy(model["components"][0]))
        errors = validate_candidate(model)
        self.assertEqual(len(errors), 2)
        self.assertTrue(all("duplicado" in error for error in errors))

    def test_uncovered_requirement_and_unknown_trace_are_accumulated(self):
        model = valid_model()
        model["components"][1]["tracesTo"] = ["R404"]
        errors = validate_candidate(model)
        self.assertTrue(any("inexistente 'R404'" in error for error in errors))
        self.assertTrue(any("'R2' no está cubierto" in error for error in errors))
        self.assertEqual(extract_model_metrics(model).coverage_percent, 50.0)

    def test_malformed_endpoints_do_not_crash_batch(self):
        model = valid_model()
        model["connectors"][0].update(source=["A"], target={"id": "B"})
        self.assertEqual(len(validate_candidate(model)), 2)

    def test_default_skips_and_revalidation_rejects_old_invalid_model(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            model = valid_model()
            source = project / "2_candidato_materializado.json"
            source.write_text(json.dumps(model), encoding="utf-8")
            process_project(project)
            accepted = project / "3_modelo_validado.json"
            original = accepted.read_bytes()
            self.assertIn("se omite", process_project(project))
            process_project(project, revalidate=True)
            self.assertEqual(accepted.read_bytes(), original)
            model["components"][1]["tracesTo"] = []
            source.write_text(json.dumps(model), encoding="utf-8")
            self.assertIn("rechazado", process_project(project, revalidate=True))
            self.assertFalse(accepted.exists())
            self.assertTrue((project / "reporte_de_errores_fase3.json").is_file())


class PumlReportTests(unittest.TestCase):
    def test_puml_counts_and_escaped_name(self):
        text = VALID_PUML.replace('"Servicio"', '"Servicio \\"Central\\""')
        result = check_generated_puml(text)
        self.assertTrue(result.is_valid, result.errors)
        self.assertEqual((result.component_count, result.connector_count), (2, 1))

    def test_invalid_puml_is_rejected(self):
        mutations = [
            VALID_PUML.replace("@enduml", ""),
            VALID_PUML.replace("A --> B", "A --> UNKNOWN"),
            VALID_PUML.replace('"Almacén" as B', '"Almacén" as A'),
            VALID_PUML.replace('"Servicio"', '"Servicio'),
        ]
        for text in mutations:
            with self.subTest(text=text):
                self.assertFalse(check_generated_puml(text).is_valid)

    def test_reference_counts_include_containers_and_distinguish_arrows(self):
        text = '''@startuml
package "Capa" as P {
rectangle "Servicio" as A
component "Cliente" as B
database "Datos" as D
}
A --> D : escribe
B ..> A : usa
A .. D
B -- A
note right of A
rectangle "Esto es una nota"
A --> B
end note
' component "Comentario"
@enduml
'''
        result = analyze_reference_puml(text)
        self.assertEqual(result.total_elements, 4)
        self.assertEqual(result.total_relations, 4)
        self.assertEqual(list(result.relation_counts.values()), [1, 1, 1, 1])

    def test_rejected_project_keeps_historical_puml_out_of_model_metrics(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            dataset = base / "dataset"
            output = base / "output"
            (dataset / "AD").mkdir(parents=True)
            output.mkdir()
            (dataset / "req_final.jsonl").write_text('{"req_id":"R1"}\n', encoding="utf-8")
            (dataset / "AD/ad.puml").write_text(VALID_PUML, encoding="utf-8")
            (output / "4_codigo_final.puml").write_text(VALID_PUML, encoding="utf-8")
            (output / "reporte_de_errores_fase3.json").write_text(
                '{"detalles":["ID duplicado"]}', encoding="utf-8"
            )
            report = build_project_report(ProjectPaths("JAVA", "Prueba", dataset, output))
            self.assertEqual(report.status, STATUS_REJECTED_PHASE3)
            self.assertIsNone(report.model)
            self.assertTrue(report.puml.is_valid)


if __name__ == "__main__":
    unittest.main()
