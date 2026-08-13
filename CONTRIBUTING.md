# Contributing Guide

## 1. Development

### Starting the bot
To start the bot, simply run: 
```bash
uv run python -X gil=0 backend/main.py
```

This will automatically install dependencies.

### Running tests
```bash
uv run python -X gil=0 backend/main.py --tests
```

## 2. Documentation

For documentation on the internal functioning of the bot, do `python -m sc docs [-h] {subsystems,feat,abstract,core} [section]`.

Run `python -m sc docs -h` for more details.
