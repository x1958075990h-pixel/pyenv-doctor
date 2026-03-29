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


def build_result(
    scanned_directory: str | None = None,
    found_files: list[str] | None = None,
    error: str | None = None,
) -> dict[str, object]:
    """Build a structured result that works for both text and JSON output."""
    # Default to an empty list so the JSON structure stays predictable.
    detected_files = found_files if found_files is not None else []

    return {
        "scanned_directory": scanned_directory,
        "found_files": detected_files,
        "looks_like_python_project": bool(detected_files),
        "virtual_environment_detected": is_virtual_environment_detected(),
        "error": error,
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


def print_virtual_environment_result() -> None:
    """Print the virtual environment detection result."""
    print()
    print("Virtual environment detection:")

    if is_virtual_environment_detected():
        print("Virtual environment: detected")
    else:
        print("Virtual environment: not detected")
        print("Recommendation: use venv or Conda for an isolated Python environment")


def main(argv: list[str] | None = None) -> int:
    """Run the program and return an exit code."""
    # Allow tests and the console script to pass arguments explicitly when needed.
    arguments = argv if argv is not None else sys.argv[1:]

    # Parse arguments now so the CLI structure stays ready for small future changes.
    parser = build_parser()
    # Detect JSON mode early so parse errors can also return JSON when requested.
    parser.json_output = "--json" in arguments
    args = parser.parse_args(arguments)

    # Scan either the provided directory or, by default, the current working directory.
    scan_path, error_message, displayed_path = get_scan_path(args.path)

    # Keep the existing non-zero exit behavior for invalid paths.
    if error_message is not None:
        if args.json:
            print_json_result(build_result(scanned_directory=displayed_path, error=error_message))
        else:
            print(error_message, file=sys.stderr)
        return 1

    # At this point the scan path is valid and safe to inspect.
    assert scan_path is not None
    found_files = find_marker_files(scan_path)

    # JSON mode returns only structured data and skips the human-readable text blocks.
    if args.json:
        print_json_result(
            build_result(
                scanned_directory=displayed_path,
                found_files=found_files,
            )
        )
        return 0

    print_project_result(scan_path, found_files)
    print_virtual_environment_result()
    return 0


if __name__ == "__main__":
    # Allow direct execution with `python main.py` and return a process exit code.
    sys.exit(main())
