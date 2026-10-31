"""Offline launcher regressions using fake CLIs; no model or network calls."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
OLD = "@startuml\n[OLD]\n@enduml\n"
NEW = "@startuml\n[NEW]\n@enduml\n"


class ForcedRerunTests(unittest.TestCase):
    def run_case(self, launcher, writes_prediction):
        shell = shutil.which("powershell") if launcher == "mini" else shutil.which("bash")
        if launcher == "openhands" and os.name == "nt":
            git = shutil.which("git")
            candidate = Path(git).resolve().parent.parent / "usr/bin/bash.exe" if git else None
            shell = str(candidate) if candidate and candidate.is_file() else None
        if not shell:
            self.skipTest(f"{launcher} test shell is unavailable")
        scratch = ROOT / "tmp"
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="launcher-test-", dir=scratch) as name:
            work = Path(name).resolve()
            self.assertTrue(work.is_relative_to(scratch.resolve()))
            inputs = work / "input/sample"
            inputs.mkdir(parents=True)
            (inputs / "checked_srs.md").write_text("A service shall store messages.\n", encoding="utf-8")
            output = work / "output"
            pred = output / "gpt-5/sample/predicted.puml"
            pred.parent.mkdir(parents=True)
            pred.write_text(OLD, encoding="utf-8")
            env = dict(os.environ, OPENAI_API_KEY="test-not-a-real-key", LLM_API_KEY="test-not-a-real-key",
                       FAKE_PRED_PATH=pred.as_posix(), FAKE_WRITE="1" if writes_prediction else "0")
            if launcher == "mini":
                fake_py = work / "fake.py"
                fake_py.write_text(
                    "import os\nfrom pathlib import Path\n"
                    "if os.environ['FAKE_WRITE'] == '1':\n"
                    f"    Path(os.environ['FAKE_PRED_PATH']).write_text({NEW!r}, encoding='utf-8')\n",
                    encoding="utf-8")
                fake = work / "fake.cmd"
                fake.write_text(f'@"{sys.executable}" "{fake_py}"\n@exit /b %errorlevel%\n', encoding="utf-8")
                command = [shell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                           str(ROOT / "generation/mini_swe.ps1"), "-Root", str(ROOT),
                           "-InputDir", str(work / "input"), "-OutputRoot", str(output),
                           "-Models", "gpt-5", "-Sample", "sample", "-MiniExe", str(fake), "-Force", "-NoApiBase"]
            else:
                fake = work / "fake-openhands.sh"
                fake.write_text("#!/usr/bin/env bash\nprintf 'Agent initialized with model: openai/gpt-5\\n'\n"
                                'if [[ "$FAKE_WRITE" == "1" ]]; then\n'
                                '  printf "@startuml\\n[NEW]\\n@enduml\\n" > "$FAKE_PRED_PATH"\nfi\n',
                                encoding="utf-8", newline="\n")
                fake.chmod(0o755)
                env.update(ROOT=ROOT.as_posix(), INPUT=(work / "input").as_posix(), OUTROOT=output.as_posix(),
                           OPENHANDS_BIN=fake.as_posix(), PYTHON_BIN=Path(sys.executable).as_posix(),
                           MODELS_OVERRIDE="gpt-5", SAMPLES_OVERRIDE="sample", FORCE="1", DRY_RUN="0",
                           DATASET="E-R2A", OH_PERSISTENCE_DIR=(work / "state").as_posix(), STOP_ON_ERROR="1")
                command = [shell, "-c", 'export PATH=/usr/bin:/bin:$PATH; exec bash "$1"',
                           "launcher-test", (ROOT / "generation/openhands.sh").as_posix()]
            result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=30)
            backups = list(pred.parent.glob("predicted.previous.*.puml"))
            self.assertEqual(len(backups), 1, result.stdout + result.stderr)
            self.assertEqual(backups[0].read_text(encoding="utf-8"), OLD)
            if writes_prediction:
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(pred.read_text(encoding="utf-8"), NEW)
            else:
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("predicted.puml is missing", result.stdout + result.stderr)
                self.assertFalse(pred.exists())

    def test_mini_rejects_stale_output(self):
        self.run_case("mini", False)

    def test_mini_accepts_fresh_output(self):
        self.run_case("mini", True)

    def test_openhands_rejects_stale_output(self):
        self.run_case("openhands", False)

    def test_openhands_accepts_fresh_output(self):
        self.run_case("openhands", True)


if __name__ == "__main__":
    unittest.main()
