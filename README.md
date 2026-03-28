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

## Requirements

- Python 3.11+

## Installation

### 1. Make sure Python is available

```powershell
python --version
```

### 2. Enter the project directory

```powershell
cd pyenv-doctor
```

### 3. Install dependencies

This MVP uses only the Python standard library, so there are no third-party packages to install.

## Run

Run the tool from the current directory:

```powershell
python main.py
```

## Testing Virtual Environment Detection

If you want to test virtual environment detection on Windows, activate the virtual environment first and then run:

```powershell
python main.py
```

This is recommended because `py -3.14 main.py` may use the system Python launcher instead of the activated virtual environment.

## Example Output

### Example 1: Python project detected, virtual environment not detected

```text
Scanned directory: C:\Users\Administrator\Documents\New project\pyenv-doctor

Project file detection:
- requirements.txt: found
- pyproject.toml: not found
- setup.py: not found
- setup.cfg: not found

Conclusion: this looks like a Python project
Reason: detected requirements.txt

Virtual environment detection:
Virtual environment: not detected
Recommendation: use venv or Conda for an isolated Python environment
```

### Example 2: Python project detected, virtual environment detected

```text
Scanned directory: C:\Users\Administrator\Documents\New project\pyenv-doctor

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

## Roadmap

- allow scanning a specific directory
- add simple exit codes
- add basic automated tests
- support JSON output

## License

This project is licensed under the [MIT License](LICENSE).
