import json
import unittest
from evaluation_script.reqcov_citations import decode_assessments, LINE_CITATION_FORMAT


class CitationEncodingTests(unittest.TestCase):
    def test_source_lines_preserve_architecture_paths(self):
        pred = '@startuml\ncomponent "/home/jovyan/work" as notebook\n@enduml\n'
        raw = json.dumps({"requirement_assessments": [{"evidence_line_numbers": [2]}]})
        value = decode_assessments(raw, pred, LINE_CITATION_FORMAT)
        self.assertEqual(value["requirement_assessments"][0]["evidence"], [pred.splitlines()[1]])

    def test_line_ids_require_explicit_encoding(self):
        raw = '{"requirement_assessments": [{"evidence": [2]}]}'
        self.assertEqual(decode_assessments(raw, "a\nb") ["requirement_assessments"][0]["evidence"], [2])
        self.assertEqual(decode_assessments(raw, "a\nb", LINE_CITATION_FORMAT)["requirement_assessments"][0]["evidence"], ["b"])

    def test_bad_indices_rejected(self):
        for index in [0, 3, True, "2"]:
            with self.subTest(index=index), self.assertRaises(ValueError):
                raw = json.dumps({"requirement_assessments": [{"evidence": [index]}]})
                decode_assessments(raw, "a\nb", LINE_CITATION_FORMAT)
