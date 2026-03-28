"""
pyenv-doctor: a minimal Python project detector.

This script scans the current directory and checks whether it
looks like a Python project based on a few common files.
"""

from pathlib import Path


def check_python_project(path: Path) -> None:
    """
    Scan a directory and print whether it looks like a Python project.
    """
    indicators = [
        "requirements.txt",
        "pyproject.toml",
        "setup.py",
        "setup.cfg",
    ]

    found_files = []

    print(f"Scan path: {path}")
    print()
    print("Check results:")

    for filename in indicators:
        file_path = path / filename

        if file_path.exists():
            print(f"- {filename}: found")
            found_files.append(filename)
        else:
            print(f"- {filename}: not found")

    print()

    if found_files:
        print("Conclusion: This looks like a Python project")
        print(f"Reason: detected {found_files[0]}")
    else:
        print("Conclusion: No obvious Python project indicators found")


def main() -> None:
    """
    Entry point of the script.
    """
    current_path = Path.cwd()
    check_python_project(current_path)


if __name__ == "__main__":
    main()
