# pyenv-doctor

`pyenv-doctor` is a minimal Python command-line tool for beginners.

It scans the current directory, checks whether it looks like a Python project, and tells you whether the current Python interpreter is running inside a virtual environment.

## What It Checks

This MVP checks for these common Python project files:

- `requirements.txt`
- `pyproject.toml`
- `setup.py`
- `setup.cfg`

If at least one of them exists, the tool prints:

`Conclusion: this looks like a Python project`

It also checks whether the current Python is running in a virtual environment.

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
|-- README.md
|-- requirements.txt
`-- main.py
```

## Installation

### 1. Make sure Python 3.11 is available

```powershell
py -3.11 --version
```

### 2. Enter the project directory

```powershell
cd pyenv-doctor
```

### 3. Install dependencies

This MVP uses only the Python standard library, so there are no third-party packages to install.

You can still run:

```powershell
py -3.11 -m pip install -r requirements.txt
```

## Run

Run the tool from the current directory:

```powershell
py -3.11 main.py
```

The command name inside the CLI is `pyenv-doctor`.

## Example Output

### Example 1: Python project detected, virtual environment detected

```text
Scanned directory: C:\demo\my-project

Project file detection:
- requirements.txt: found
- pyproject.toml: not found
- setup.py: not found
- setup.cfg: not found

Conclusion: this looks like a Python project
Reason: detected requirements.txt

Virtual environment detection:
Virtual environment: detected
```

### Example 2: No project markers, no virtual environment

```text
Scanned directory: C:\demo\empty-folder

Project file detection:
- requirements.txt: not found
- pyproject.toml: not found
- setup.py: not found
- setup.cfg: not found

Conclusion: no clear Python project markers were found
Details: common Python project files were not found in this directory.

Virtual environment detection:
Virtual environment: not detected
Recommendation: use venv or Conda for an isolated Python environment
```

## Roadmap

- Allow scanning a specific directory
- Add simple exit codes
- Add basic automated tests
- Support JSON output
