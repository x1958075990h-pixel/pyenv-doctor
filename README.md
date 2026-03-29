# pyenv-doctor

[![PyPI version](https://img.shields.io/pypi/v/python-project-doctor-cli)](https://pypi.org/project/python-project-doctor-cli/)
[![Python versions](https://img.shields.io/pypi/pyversions/python-project-doctor-cli)](https://pypi.org/project/python-project-doctor-cli/)
[![CI](https://github.com/x1958075990h-pixel/pyenv-doctor/actions/workflows/ci.yml/badge.svg)](https://github.com/x1958075990h-pixel/pyenv-doctor/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/x1958075990h-pixel/pyenv-doctor)](LICENSE)

A beginner-friendly CLI that checks whether a directory looks like a Python project, detects virtual environments, and suggests what to do next.

## Quick Start

Install from PyPI:

```powershell
python -m pip install python-project-doctor-cli
```

Run it on the current directory:

```powershell
pyenv-doctor .
```

Get machine-readable output:

```powershell
pyenv-doctor . --json
```

## Why Use It

`pyenv-doctor` is useful when you want to quickly answer questions like:

- Does this folder look like a Python project?
- Am I running Python inside a virtual environment?
- What should I try next?

It is designed to stay small, readable, and friendly to beginners.

## What It Checks

This MVP checks for these common Python project files:

- `requirements.txt`
- `pyproject.toml`
- `setup.py`
- `setup.cfg`
- `Pipfile`
- `poetry.lock`
- `uv.lock`
- `environment.yml`
- `.python-version`

If at least one of them exists, the tool prints:

`Conclusion: this looks like a Python project`

It also checks whether the current Python interpreter is running inside a virtual environment.
After the scan, it prints a short list of beginner-friendly suggestions based on the result.

Supported common cases:

- `venv`
- `virtualenv`
- `Conda`

## Project Structure

```text
pyenv-doctor/
|-- .gitignore
|-- .github/
|   |-- workflows/
|   |   |-- ci.yml
|   |   `-- publish.yml
|-- AGENTS.md
|-- pyproject.toml
|-- README.md
|-- requirements.txt
|-- LICENSE
|-- main.py
`-- tests/
    `-- test_main.py
```

## Installation

### 1. Make sure Python 3.11 or newer is available

```powershell
python --version
```

### 2. Install from PyPI

The PyPI package name is:

```text
python-project-doctor-cli
```

Install it with:

```powershell
python -m pip install python-project-doctor-cli
```

The installed command name is still:

```powershell
pyenv-doctor
```

### 3. Install locally from source

Clone the repository, enter the project directory, and install it locally:

```powershell
python -m pip install .
```

For local development, you can also use editable install:

```powershell
python -m pip install -e .
```

## Run

Run the installed CLI command:

```powershell
pyenv-doctor
pyenv-doctor .
pyenv-doctor C:\my-project
pyenv-doctor . --json
```

Run the tool from source:

```powershell
python main.py
python main.py C:\my-project
python main.py C:\my-project --json
```

### Windows note for virtual environment detection

If you want to verify virtual environment detection on Windows, activate the virtual environment first and then run:

```powershell
python main.py
```

This is recommended because `py -3.14 main.py` may use the system interpreter instead of the currently activated virtual environment.

## Run Tests

Run the test suite with:

```powershell
python -m unittest discover -s tests -v
```

## Exit Codes

- `0`: the scan completed successfully
- non-zero: the scan failed because the path was invalid or the arguments were invalid

## JSON Output

Use `--json` to get machine-readable output:

```powershell
pyenv-doctor . --json
python main.py . --json
```

The JSON output includes:

- `scanned_directory`
- `found_files`
- `looks_like_python_project`
- `virtual_environment_detected`
- `error`
- `suggestions`

## Example Output

### Example 1: Python project detected, virtual environment detected

```text
Scanned directory: C:\demo\my-project

Project file detection:
- requirements.txt: not found
- pyproject.toml: found
- setup.py: not found
- setup.cfg: not found
- Pipfile: not found
- poetry.lock: found
- uv.lock: not found
- environment.yml: not found
- .python-version: not found

Conclusion: this looks like a Python project
Reason: detected pyproject.toml, poetry.lock

Virtual environment detection:
Virtual environment: detected

Suggestions:
- Open pyproject.toml to check how this project should be installed or run.
- If this project uses Poetry, review pyproject.toml and try poetry install.
```

### Example 2: No project markers, no virtual environment

```text
Scanned directory: C:\demo\empty-folder

Project file detection:
- requirements.txt: not found
- pyproject.toml: not found
- setup.py: not found
- setup.cfg: not found
- Pipfile: not found
- poetry.lock: not found
- uv.lock: not found
- environment.yml: not found
- .python-version: not found

Conclusion: no clear Python project markers were found
Details: common Python project files were not found in this directory.

Virtual environment detection:
Virtual environment: not detected
Recommendation: use venv or Conda for an isolated Python environment

Suggestions:
- Verify that you are scanning the project root directory.
```

### Example 3: Invalid path

```text
Error: path does not exist: C:\does-not-exist

Suggestions:
- Check the path spelling and try again.
```

### Example 4: JSON output

```json
{
  "scanned_directory": "C:\\demo\\my-project",
  "found_files": [
    "Pipfile",
    ".python-version"
  ],
  "looks_like_python_project": true,
  "virtual_environment_detected": false,
  "error": null,
  "suggestions": [
    "Open Pipfile to review the project's dependencies and environment settings.",
    "Check .python-version to see which Python version this project expects."
  ]
}
```

## Publishing

This repository includes a GitHub Actions workflow for trusted publishing to PyPI when a GitHub release is published.

To use it, first add this repository as a trusted publisher in your PyPI project settings.
Then create a GitHub release to trigger the publish workflow.

## Roadmap

- Improve test coverage
- Improve detection rules for different Python workflows

## License

This project is licensed under the [MIT License](LICENSE).
