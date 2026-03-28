# pyenv-doctor

`pyenv-doctor` is a minimal Python CLI tool for beginners.

It scans the current directory and checks whether it looks like a Python project based on a few common files.

This version is an early MVP and focuses only on simple project detection.

## Features

Currently, this tool checks whether the following files exist:

- `requirements.txt`
- `pyproject.toml`
- `setup.py`
- `setup.cfg`

If at least one of them is found, the tool prints:

```text
This looks like a Python project
```

If none of them are found, the tool prints:

```text
No obvious Python project indicators found
```

## Project Structure

```text
pyenv-doctor/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── main.py
```

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

## Example Output

When a matching file is found:

```text
Scan path: C:\Users\Administrator\Documents\New project\pyenv-doctor

Check results:
- requirements.txt: found
- pyproject.toml: not found
- setup.py: not found
- setup.cfg: not found

Conclusion: This looks like a Python project
Reason: detected requirements.txt
```

When no matching file is found:

```text
Scan path: C:\some\other\folder

Check results:
- requirements.txt: not found
- pyproject.toml: not found
- setup.py: not found
- setup.cfg: not found

Conclusion: No obvious Python project indicators found
```

## Current Limitations

This MVP does not support:

- virtual environment detection
- Python version checking
- automatic fixes
- Poetry, Conda, or uv detection
- global command installation

## Roadmap

Planned next steps:

- add virtual environment detection
- add Python version checks
- support scanning a custom path
- improve output formatting
- package it as a real CLI command

## License

This project is licensed under the [MIT License](LICENSE).
