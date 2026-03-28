# pyenv-doctor

`pyenv-doctor` is a beginner-friendly Python CLI tool.

It scans a directory and checks whether it looks like a Python project based on a few common files.  
It also detects whether the current Python process is running inside a virtual environment.

This version is still an early MVP and focuses on simple, readable output.

## Features

Currently, this tool can:

- detect common Python project indicator files
- detect whether Python is running inside a virtual environment
- show simple English output for beginners

The following project files are checked:

- `requirements.txt`
- `pyproject.toml`
- `setup.py`
- `setup.cfg`

## Requirements

- Python 3.11+

## How to Run

Run the script inside the project directory:

```bash
python main.py
```

On Windows, you can also run:

```bash
py -3.14 main.py
```

## Virtual Environment Notes

If you want to test virtual environment detection, activate the virtual environment first and then run:

```bash
python main.py
```

This is important on Windows because `py -3.14 main.py` may use the system Python launcher instead of the activated virtual environment.

## Example Output

When a matching file is found and no virtual environment is active:

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

When a virtual environment is active:

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

## Project Structure

```text
pyenv-doctor/
├── .gitignore
├── README.md
├── requirements.txt
└── main.py
```

## Current Limitations

This MVP does not support:

- scanning a custom path yet
- Python version compatibility checks
- automatic fixes
- Poetry, uv, or Conda project detection
- global command installation

## Roadmap

Planned next steps:

- support scanning a custom path
- improve output formatting
- add Python version checks
- package it as a real CLI command

## Should `.venv` be uploaded?

No.  
You should **not** upload the `.venv` folder to GitHub.

A virtual environment contains local interpreter files and installed packages that are specific to your computer.  
It is usually large and should stay ignored by `.gitignore`.

## License

MIT
