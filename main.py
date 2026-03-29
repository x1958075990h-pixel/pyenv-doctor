"""Minimal command-line entry point for pyenv-doctor."""

import argparse
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


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="pyenv-doctor",
        description="Scan a directory and check whether it looks like a Python project.",
    )
    # This optional path keeps the CLI simple: no argument means current directory.
    parser.add_argument(
        "path",
        nargs="?",
        help="Optional directory path to scan. If omitted, the current directory is used.",
    )
    return parser


def get_scan_path(parser: argparse.ArgumentParser, path_argument: str | None) -> Path:
    """Return the directory to scan or exit with a clear error message."""
    # If no path was provided, keep the original behavior and scan the current directory.
    if path_argument is None:
        return Path.cwd()

    # Expand user input so paths like `~` work on supported systems.
    scan_path = Path(path_argument).expanduser()

    # Stop early with a readable error when the path does not exist.
    if not scan_path.exists():
        parser.exit(status=1, message=f"Error: path does not exist: {scan_path}\n")

    # Stop early when the path exists but is not a directory.
    if not scan_path.is_dir():
        parser.exit(status=1, message=f"Error: path is not a directory: {scan_path}\n")

    # Resolve the final directory so the output shows a clear absolute path.
    return scan_path.resolve()


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


def main() -> int:
    """Run the program and return an exit code."""
    # Parse arguments now so the CLI structure stays ready for small future changes.
    parser = build_parser()
    args = parser.parse_args()

    # Scan either the provided directory or, by default, the current working directory.
    scan_path = get_scan_path(parser, args.path)
    found_files = find_marker_files(scan_path)
    print_project_result(scan_path, found_files)
    print_virtual_environment_result()
    return 0


if __name__ == "__main__":
    # Allow direct execution with `python main.py` and return a process exit code.
    sys.exit(main())
