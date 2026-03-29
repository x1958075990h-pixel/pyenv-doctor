"""Minimal command-line entry point for pyenv-doctor."""

import argparse
import json
import os
import sys
from pathlib import Path


# These files are the simplest markers for a Python project in this MVP.
PROJECT_MARKER_FILES = [
    "requirements.txt",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "Pipfile",
    "poetry.lock",
    "uv.lock",
    "environment.yml",
    ".python-version",
]


class JsonAwareArgumentParser(argparse.ArgumentParser):
    """Argument parser that can return JSON-formatted errors when requested."""

    def __init__(self, *args, **kwargs) -> None:
        """Create the parser and remember whether JSON mode is requested."""
        super().__init__(*args, **kwargs)
        self.json_output = False

    def error(self, message: str) -> None:
        """Print a JSON error instead of plain text when JSON mode is enabled."""
        if self.json_output:
            print_json_result(build_result(error=f"Argument error: {message}"))
            raise SystemExit(2)

        super().error(message)


def build_parser() -> JsonAwareArgumentParser:
    """Create the command-line argument parser."""
    parser = JsonAwareArgumentParser(
        prog="pyenv-doctor",
        description="Scan a directory and check whether it looks like a Python project.",
    )
    # This optional path keeps the CLI simple: no argument means current directory.
    parser.add_argument(
        "path",
        nargs="?",
        help="Optional directory path to scan. If omitted, the current directory is used.",
    )
    # This flag switches the output from human-readable text to structured JSON.
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the result as JSON.",
    )
    return parser


def get_scan_path(path_argument: str | None) -> tuple[Path | None, str | None, str | None]:
    """Return the scan path, an optional error message, and the displayed path string."""
    # If no path was provided, keep the original behavior and scan the current directory.
    if path_argument is None:
        scan_path = Path.cwd().resolve()
        return scan_path, None, str(scan_path)

    # Expand user input so paths like `~` work on supported systems.
    scan_path = Path(path_argument).expanduser()

    # Return a clear error when the path does not exist.
    if not scan_path.exists():
        return None, f"Error: path does not exist: {scan_path}", str(scan_path)

    # Return a clear error when the path exists but is not a directory.
    if not scan_path.is_dir():
        return None, f"Error: path is not a directory: {scan_path}", str(scan_path)

    # Resolve the final directory so the output shows a clear absolute path.
    resolved_path = scan_path.resolve()
    return resolved_path, None, str(resolved_path)


def find_marker_files(scan_path: Path) -> list[str]:
    """Return the project marker files found in the current directory."""
    found_files: list[str] = []

    # Check each file one by one so the logic stays easy to read.
    for file_name in PROJECT_MARKER_FILES:
        if (scan_path / file_name).is_file():
            found_files.append(file_name)

    return found_files


def is_virtual_environment_detected() -> bool:
    """Return True when the current Python looks like it runs in a virtual environment."""
    # Conda usually exposes these environment variables when an environment is active.
    if os.environ.get("CONDA_PREFIX") or os.environ.get("CONDA_DEFAULT_ENV"):
        return True

    # venv changes sys.prefix while keeping the original value in sys.base_prefix.
    if getattr(sys, "base_prefix", sys.prefix) != sys.prefix:
        return True

    # Older virtualenv versions may set sys.real_prefix.
    if hasattr(sys, "real_prefix"):
        return True

    return False


def build_suggestions(
    found_files: list[str] | None = None,
    error: str | None = None,
    virtual_environment_detected: bool = False,
) -> list[str]:
    """Build a short list of beginner-friendly next steps."""
    detected_files = found_files if found_files is not None else []

    # Error suggestions should stay focused on fixing the immediate problem first.
    if error is not None:
        if "path does not exist" in error:
            return ["Check the path spelling and try again."]
        if "path is not a directory" in error:
            return ["Pass the project directory path instead of a single file."]
        if "Argument error:" in error:
            return ["Run pyenv-doctor --help to review the available arguments."]
        return []

    suggestions: list[str] = []

    # If nothing was detected, the safest first step is to confirm the scan location.
    if not detected_files:
        suggestions.append("Verify that you are scanning the project root directory.")

    # pyproject.toml often defines the project's preferred install and run workflow.
    if "pyproject.toml" in detected_files:
        suggestions.append("Open pyproject.toml to check how this project should be installed or run.")

    # Pipfile usually means the project expects a Pipenv-style workflow.
    if "Pipfile" in detected_files:
        suggestions.append("Open Pipfile to review the project's dependencies and environment settings.")

    # poetry.lock usually appears in Poetry-based projects.
    if "poetry.lock" in detected_files:
        suggestions.append("If this project uses Poetry, review pyproject.toml and try poetry install.")

    # uv.lock usually appears in uv-managed projects.
    if "uv.lock" in detected_files:
        suggestions.append("If this project uses uv, review the project instructions and try uv sync.")

    # environment.yml usually points to a Conda environment definition.
    if "environment.yml" in detected_files:
        suggestions.append("If this project uses Conda, create the environment from environment.yml before running it.")

    # .python-version often records the expected Python version for the project.
    if ".python-version" in detected_files:
        suggestions.append("Check .python-version to see which Python version this project expects.")

    # Only suggest a virtual environment when one is not already active.
    if "requirements.txt" in detected_files and not virtual_environment_detected:
        suggestions.append("Create and activate a virtual environment before installing dependencies.")

    return suggestions


def build_result(
    scanned_directory: str | None = None,
    found_files: list[str] | None = None,
    error: str | None = None,
    virtual_environment_detected: bool | None = None,
) -> dict[str, object]:
    """Build a structured result that works for both text and JSON output."""
    # Default to an empty list so the JSON structure stays predictable.
    detected_files = found_files if found_files is not None else []
    env_detected = (
        virtual_environment_detected
        if virtual_environment_detected is not None
        else is_virtual_environment_detected()
    )
    suggestions = build_suggestions(
        found_files=detected_files,
        error=error,
        virtual_environment_detected=env_detected,
    )

    return {
        "scanned_directory": scanned_directory,
        "found_files": detected_files,
        "looks_like_python_project": bool(detected_files),
        "virtual_environment_detected": env_detected,
        "error": error,
        "suggestions": suggestions,
    }


def print_json_result(result: dict[str, object]) -> None:
    """Print a JSON result with stable formatting for humans and scripts."""
    # Indented JSON stays readable while still being valid machine output.
    print(json.dumps(result, indent=2))


def print_project_result(scan_path: Path, found_files: list[str]) -> None:
    """Print the project file detection result in a clear format."""
    print(f"Scanned directory: {scan_path}")
    print()
    print("Project file detection:")

    # Print the status for every marker file in a fixed order.
    for file_name in PROJECT_MARKER_FILES:
        status = "found" if file_name in found_files else "not found"
        print(f"- {file_name}: {status}")

    print()

    # If at least one marker file exists, the directory probably is a Python project.
    if found_files:
        print("Conclusion: this looks like a Python project")
        print(f"Reason: detected {', '.join(found_files)}")
    else:
        print("Conclusion: no clear Python project markers were found")
        print("Details: common Python project files were not found in this directory.")


def print_virtual_environment_result(virtual_environment_detected: bool) -> None:
    """Print the virtual environment detection result."""
    print()
    print("Virtual environment detection:")

    if virtual_environment_detected:
        print("Virtual environment: detected")
    else:
        print("Virtual environment: not detected")
        print("Recommendation: use venv or Conda for an isolated Python environment")


def print_suggestions(suggestions: list[str], stream=None) -> None:
    """Print a short suggestions section after the main result."""
    output_stream = stream if stream is not None else sys.stdout
    print(file=output_stream)
    print("Suggestions:", file=output_stream)

    if not suggestions:
        print("- No immediate suggestions.", file=output_stream)
        return

    # Keep each suggestion short and actionable for beginners.
    for suggestion in suggestions:
        print(f"- {suggestion}", file=output_stream)


def main(argv: list[str] | None = None) -> int:
    """Run the program and return an exit code."""
    # Allow tests and the console script to pass arguments explicitly when needed.
    arguments = argv if argv is not None else sys.argv[1:]

    # Parse arguments now so the CLI structure stays ready for small future changes.
    parser = build_parser()
    # Detect JSON mode early so parse errors can also return JSON when requested.
    parser.json_output = "--json" in arguments
    args = parser.parse_args(arguments)
    virtual_environment_detected = is_virtual_environment_detected()

    # Scan either the provided directory or, by default, the current working directory.
    scan_path, error_message, displayed_path = get_scan_path(args.path)

    # Keep the existing non-zero exit behavior for invalid paths.
    if error_message is not None:
        error_result = build_result(
            scanned_directory=displayed_path,
            error=error_message,
            virtual_environment_detected=virtual_environment_detected,
        )
        if args.json:
            print_json_result(error_result)
        else:
            print(error_message, file=sys.stderr)
            print_suggestions(error_result["suggestions"], stream=sys.stderr)
        return 1

    # At this point the scan path is valid and safe to inspect.
    assert scan_path is not None
    found_files = find_marker_files(scan_path)
    result = build_result(
        scanned_directory=displayed_path,
        found_files=found_files,
        virtual_environment_detected=virtual_environment_detected,
    )

    # JSON mode returns only structured data and skips the human-readable text blocks.
    if args.json:
        print_json_result(result)
        return 0

    print_project_result(scan_path, found_files)
    print_virtual_environment_result(virtual_environment_detected)
    print_suggestions(result["suggestions"])
    return 0


if __name__ == "__main__":
    # Allow direct execution with `python main.py` and return a process exit code.
    sys.exit(main())
