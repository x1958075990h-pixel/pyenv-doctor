"""Minimal tests for the pyenv-doctor command-line tool."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


# These paths point to the project root and the CLI entry file.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MAIN_SCRIPT = PROJECT_ROOT / "main.py"


class PyenvDoctorCliTests(unittest.TestCase):
    """Test the current beginner-friendly CLI behavior."""

    def run_cli(
        self,
        *args: str,
        cwd: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """Run the CLI with optional arguments and return the result."""
        # By default, run from the project root to match normal local usage.
        working_directory = cwd if cwd is not None else PROJECT_ROOT

        return subprocess.run(
            [sys.executable, str(MAIN_SCRIPT), *args],
            cwd=working_directory,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_scan_current_directory_succeeds(self) -> None:
        """The CLI should scan the current directory when no path is passed."""
        result = self.run_cli(cwd=PROJECT_ROOT)

        self.assertEqual(result.returncode, 0)
        self.assertIn(f"Scanned directory: {PROJECT_ROOT.resolve()}", result.stdout)
        self.assertIn("Project file detection:", result.stdout)
        self.assertIn("Virtual environment detection:", result.stdout)

    def test_scan_specific_directory_succeeds(self) -> None:
        """The CLI should scan a provided directory path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            scan_path = Path(temp_dir)
            result = self.run_cli(str(scan_path))

            self.assertEqual(result.returncode, 0)
            self.assertIn(f"Scanned directory: {scan_path.resolve()}", result.stdout)
            self.assertIn(
                "Conclusion: no clear Python project markers were found",
                result.stdout,
            )

    def test_nonexistent_path_returns_non_zero(self) -> None:
        """A missing path should return a non-zero exit code and a clear error."""
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_path = Path(temp_dir) / "missing-folder"
            result = self.run_cli(str(missing_path))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Error: path does not exist:", result.stderr)

    def test_file_path_returns_non_zero(self) -> None:
        """A file path should return a non-zero exit code and a clear error."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "example.txt"

            # Create a normal file so the CLI can show the "not a directory" error.
            file_path.write_text("example", encoding="utf-8")
            result = self.run_cli(str(file_path))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Error: path is not a directory:", result.stderr)

    def test_marker_file_is_detected(self) -> None:
        """At least one known project marker file should be detected."""
        with tempfile.TemporaryDirectory() as temp_dir:
            scan_path = Path(temp_dir)
            marker_file = scan_path / "requirements.txt"

            # A single marker file is enough for the current MVP to detect a project.
            marker_file.write_text("# test marker\n", encoding="utf-8")
            result = self.run_cli(str(scan_path))

            self.assertEqual(result.returncode, 0)
            self.assertIn("- requirements.txt: found", result.stdout)
            self.assertIn("Conclusion: this looks like a Python project", result.stdout)

    def test_json_output_for_successful_scan(self) -> None:
        """JSON mode should return structured output for a valid directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            scan_path = Path(temp_dir)
            result = self.run_cli(str(scan_path), "--json")

            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stderr, "")

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scanned_directory"], str(scan_path.resolve()))
            self.assertEqual(payload["found_files"], [])
            self.assertFalse(payload["looks_like_python_project"])
            self.assertIsInstance(payload["virtual_environment_detected"], bool)
            self.assertIsNone(payload["error"])

    def test_json_output_detects_marker_file(self) -> None:
        """JSON mode should include marker files and project detection status."""
        with tempfile.TemporaryDirectory() as temp_dir:
            scan_path = Path(temp_dir)
            marker_file = scan_path / "pyproject.toml"

            # Use one marker file so the JSON result stays easy to verify.
            marker_file.write_text("[project]\nname = 'demo'\n", encoding="utf-8")
            result = self.run_cli(str(scan_path), "--json")

            self.assertEqual(result.returncode, 0)

            payload = json.loads(result.stdout)
            self.assertEqual(payload["found_files"], ["pyproject.toml"])
            self.assertTrue(payload["looks_like_python_project"])
            self.assertIsNone(payload["error"])

    def test_json_output_for_missing_path(self) -> None:
        """JSON mode should return a structured error for a missing path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_path = Path(temp_dir) / "missing-folder"
            result = self.run_cli(str(missing_path), "--json")

            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stderr, "")

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scanned_directory"], str(missing_path))
            self.assertEqual(payload["found_files"], [])
            self.assertFalse(payload["looks_like_python_project"])
            self.assertIn("Error: path does not exist:", payload["error"])

    def test_json_output_for_file_path(self) -> None:
        """JSON mode should return a structured error for a file path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "example.txt"

            # Create a file so the CLI can report that the path is not a directory.
            file_path.write_text("example", encoding="utf-8")
            result = self.run_cli(str(file_path), "--json")

            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stderr, "")

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scanned_directory"], str(file_path))
            self.assertEqual(payload["found_files"], [])
            self.assertFalse(payload["looks_like_python_project"])
            self.assertIn("Error: path is not a directory:", payload["error"])

    def test_json_output_for_argument_error(self) -> None:
        """JSON mode should return structured output for argument parsing errors."""
        result = self.run_cli("one", "two", "--json")

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stderr, "")

        payload = json.loads(result.stdout)
        self.assertIsNone(payload["scanned_directory"])
        self.assertEqual(payload["found_files"], [])
        self.assertFalse(payload["looks_like_python_project"])
        self.assertIn("Argument error:", payload["error"])


if __name__ == "__main__":
    unittest.main()
