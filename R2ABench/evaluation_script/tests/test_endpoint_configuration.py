import os
import unittest
from unittest.mock import patch
from evaluation_script.l1_structural import L1AlignmentConfig, L1AlignmentError, _call_alignment_judge
from evaluation_script.l2_semantic import L2JudgeConfig, _chat_completion


class EndpointConfigurationTests(unittest.TestCase):
    def test_no_bundled_endpoint_or_credential(self):
        with patch.dict(os.environ, {}, clear=True):
            for cls in [L1AlignmentConfig, L2JudgeConfig]:
                config=cls.from_env(enabled=True)
                self.assertEqual(config.base_url, "")
                self.assertIsNone(config.api_key)

    def test_l1_requires_explicit_endpoint_before_network(self):
        with patch("urllib.request.urlopen") as network, self.assertRaisesRegex(L1AlignmentError, "OPENAI_BASE_URL"):
            _call_alignment_judge(prd_summary="requirements", gt_nodes=[], predicted_nodes=[], config=L1AlignmentConfig())
        network.assert_not_called()

    def test_l2_requires_explicit_endpoint_before_network(self):
        with patch("urllib.request.urlopen") as network, self.assertRaisesRegex(ValueError, "OPENAI_BASE_URL"):
            _chat_completion("requirements", L2JudgeConfig())
        network.assert_not_called()
