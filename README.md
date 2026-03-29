# pyenv-doctor

`pyenv-doctor` is a minimal Python command-line tool for beginners.

It scans a directory, checks whether it looks like a Python project, and tells you whether the current Python interpreter is running inside a virtual environment.

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

It also checks whether the current Python is running in a virtual environment.
After the scan, it prints a short list of beginner-friendly suggestions based on the result.

Supported common cases:

- `venv`
- `virtualenv`
- `Conda`

## Why Virtual Environments Are Useful

Virtual environments help keep project dependencies isolated.
This makes it easier to avoid version conflicts between different Python projects on the same machine.

## Project Structure

```text
pyenv-doctor/
|-- .gitignore
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- pyproject.toml
|-- README.md
|-- requirements.txt
|-- main.py
`-- tests/
    `-- test_main.py
```

## Installation

### 1. Make sure Python 3.11 or newer is available

```powershell
python --version
```

### 2. Enter the project directory

```powershell
cd pyenv-doctor
```

### 3. Install dependencies

This MVP uses only the Python standard library, so there are no third-party packages to install.

You can still run:

```powershell
python -m pip install -r requirements.txt
```

### 4. Install the CLI locally

Install the project from the current directory:

```powershell
python -m pip install .
```

For local development, you can also use editable install:

```powershell
python -m pip install -e .
```

## Run

Run the tool from the current directory:

```powershell
python main.py
```

Run the installed CLI command:

```powershell
pyenv-doctor
pyenv-doctor .
pyenv-doctor C:\my-project
pyenv-doctor . --json
```

Scan a custom path:

```powershell
python main.py C:\my-project
python main.py C:\my-project --json
```

The installed command name is `pyenv-doctor`.

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

## Roadmap

- Improve test coverage
- Improve detection rules for different Python workflows
