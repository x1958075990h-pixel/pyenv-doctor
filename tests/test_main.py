"""Minimal tests for the pyenv-doctor command-line tool."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import main as cli_main


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
        self.assertIn("Suggestions:", result.stdout)

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
            self.assertIn(
                "Verify that you are scanning the project root directory.",
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

    def test_new_marker_files_are_detected_in_text_output(self) -> None:
        """The text output should list the new marker files and matching suggestions."""
        with tempfile.TemporaryDirectory() as temp_dir:
            scan_path = Path(temp_dir)
            new_marker_files = [
                "Pipfile",
                "poetry.lock",
                "uv.lock",
                "environment.yml",
                ".python-version",
            ]

            for file_name in new_marker_files:
                (scan_path / file_name).write_text("test\n", encoding="utf-8")

            result = self.run_cli(str(scan_path))

            self.assertEqual(result.returncode, 0)
            self.assertIn("- Pipfile: found", result.stdout)
            self.assertIn("- poetry.lock: found", result.stdout)
            self.assertIn("- uv.lock: found", result.stdout)
            self.assertIn("- environment.yml: found", result.stdout)
            self.assertIn("- .python-version: found", result.stdout)
            self.assertIn(
                "Open Pipfile to review the project's dependencies and environment settings.",
                result.stdout,
            )
            self.assertIn(
                "If this project uses Poetry, review pyproject.toml and try poetry install.",
                result.stdout,
            )
            self.assertIn(
                "If this project uses uv, review the project instructions and try uv sync.",
                result.stdout,
            )
            self.assertIn(
                "If this project uses Conda, create the environment from environment.yml before running it.",
                result.stdout,
            )
            self.assertIn(
                "Check .python-version to see which Python version this project expects.",
                result.stdout,
            )

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
            self.assertEqual(
                payload["suggestions"],
                ["Verify that you are scanning the project root directory."],
            )

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
            self.assertEqual(
                payload["suggestions"],
                ["Open pyproject.toml to check how this project should be installed or run."],
            )

    def test_json_output_includes_new_marker_files(self) -> None:
        """JSON mode should include the new marker files and their suggestions."""
        with tempfile.TemporaryDirectory() as temp_dir:
            scan_path = Path(temp_dir)

            for file_name in [
                "Pipfile",
                "poetry.lock",
                "uv.lock",
                "environment.yml",
                ".python-version",
            ]:
                (scan_path / file_name).write_text("test\n", encoding="utf-8")

            result = self.run_cli(str(scan_path), "--json")

            self.assertEqual(result.returncode, 0)

            payload = json.loads(result.stdout)
            self.assertEqual(
                payload["found_files"],
                [
                    "Pipfile",
                    "poetry.lock",
                    "uv.lock",
                    "environment.yml",
                    ".python-version",
                ],
            )
            self.assertTrue(payload["looks_like_python_project"])
            self.assertEqual(
                payload["suggestions"],
                [
                    "Open Pipfile to review the project's dependencies and environment settings.",
                    "If this project uses Poetry, review pyproject.toml and try poetry install.",
                    "If this project uses uv, review the project instructions and try uv sync.",
                    "If this project uses Conda, create the environment from environment.yml before running it.",
                    "Check .python-version to see which Python version this project expects.",
                ],
            )

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
            self.assertEqual(payload["suggestions"], ["Check the path spelling and try again."])

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
            self.assertEqual(
                payload["suggestions"],
                ["Pass the project directory path instead of a single file."],
            )

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
        self.assertEqual(
            payload["suggestions"],
            ["Run pyenv-doctor --help to review the available arguments."],
        )

    def test_requirements_suggestion_without_virtual_environment(self) -> None:
        """Requirements files should suggest using a virtual environment when needed."""
        suggestions = cli_main.build_suggestions(
            found_files=["requirements.txt"],
            virtual_environment_detected=False,
        )

        self.assertIn(
            "Create and activate a virtual environment before installing dependencies.",
            suggestions,
        )

    def test_requirements_suggestion_is_skipped_inside_virtual_environment(self) -> None:
        """The tool should not repeat virtual environment setup advice when already active."""
        suggestions = cli_main.build_suggestions(
            found_files=["requirements.txt"],
            virtual_environment_detected=True,
        )

        self.assertNotIn(
            "Create and activate a virtual environment before installing dependencies.",
            suggestions,
        )

    def test_pyproject_suggestion_is_included(self) -> None:
        """pyproject.toml should trigger a simple install or run suggestion."""
        suggestions = cli_main.build_suggestions(
            found_files=["pyproject.toml"],
            virtual_environment_detected=True,
        )

        self.assertIn(
            "Open pyproject.toml to check how this project should be installed or run.",
            suggestions,
        )

    def test_new_marker_suggestions_are_included(self) -> None:
        """The new marker files should generate short, actionable suggestions."""
        suggestions = cli_main.build_suggestions(
            found_files=[
                "Pipfile",
                "poetry.lock",
                "uv.lock",
                "environment.yml",
                ".python-version",
            ],
            virtual_environment_detected=True,
        )

        self.assertIn(
            "Open Pipfile to review the project's dependencies and environment settings.",
            suggestions,
        )
        self.assertIn(
            "If this project uses Poetry, review pyproject.toml and try poetry install.",
            suggestions,
        )
        self.assertIn(
            "If this project uses uv, review the project instructions and try uv sync.",
            suggestions,
        )
        self.assertIn(
            "If this project uses Conda, create the environment from environment.yml before running it.",
            suggestions,
        )
        self.assertIn(
            "Check .python-version to see which Python version this project expects.",
            suggestions,
        )


if __name__ == "__main__":
    unittest.main()
