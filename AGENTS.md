# AGENTS.md

## Project Purpose

This repository contains a beginner-friendly Python CLI tool.
The tool checks whether a directory looks like a Python project, detects virtual environments, and suggests what to do next.

## Development Rules

1. Do not redesign or rewrite the whole project.
2. Keep each change small and focused.
3. Preserve existing behavior unless the task explicitly asks for a change.
4. Keep the code easy to read for beginners.
5. Do not create duplicate files such as `main_fixed.py` or `README_fixed.md`.
6. Avoid third-party dependencies unless they are clearly necessary.
7. Keep all user-facing output in English.
8. Update `README.md` when behavior or usage changes.
9. Add or update tests when logic changes.
10. Prefer simple, incremental improvements.

## Testing

Run tests with:

```bash
python -m unittest discover -s tests -v
```

## Packaging

The PyPI package name is `python-project-doctor-cli`.
The installed CLI command remains `pyenv-doctor`.

## Contribution Style

- Prefer direct, practical changes over abstract refactors.
- Keep CLI messages short and clear.
- Keep README examples realistic and copyable.
- Preserve compatibility with the current single-file CLI structure unless a task explicitly requires a change.
