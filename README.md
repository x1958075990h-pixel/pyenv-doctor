# pyenv-doctor

`pyenv-doctor` is a minimal Python command-line tool for beginners.

It scans a directory, checks whether it looks like a Python project, and tells you whether the current Python interpreter is running inside a virtual environment.

## Current Features

This MVP currently supports:

- scanning the current working directory
- scanning a custom directory path
- detecting common Python project marker files
- detecting whether Python is running inside a virtual environment
- showing clear English error messages for invalid paths
- returning exit codes for success and failure cases

The project marker files checked are:

- `requirements.txt`
- `pyproject.toml`
- `setup.py`
- `setup.cfg`

Supported virtual environment cases:

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

Tested on:

- Python 3.14

## Installation

This MVP uses only the Python standard library, so there are no third-party dependencies to install.

To check whether Python is available:

```powershell
python --version
```

## Run

Run the tool from the current directory:

```powershell
python main.py
```

Scan the current directory explicitly:

```powershell
python main.py .
```

Scan a custom path:

```powershell
python main.py "C:\Users\Administrator\Documents\New project\pyenv-doctor"
```

## Exit Codes

The CLI uses simple process exit codes:

- `0` — the scan completed successfully
- non-zero — the scan failed because the path was invalid or the arguments were invalid

## Windows Virtual Environment Note

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

### Example 3: Invalid path

```powershell
python main.py C:\not-exists-folder
```

```text
Error: path does not exist: C:\not-exists-folder
```

### Example 4: Path is not a directory

```powershell
python main.py C:\path\to\file.txt
```

```text
Error: path is not a directory: C:\path\to\file.txt
```

## Current Limitations

This MVP does not yet support:

- JSON output
- automated tests
- repair suggestions
- packaging as an installable `pyenv-doctor` command

## Roadmap

- add basic automated tests
- support JSON output
- package the project as a real CLI command
- add simple repair suggestions for common problems

## License

This project is licensed under the [MIT License](LICENSE).
