# md-to-confluence

`md-to-confluence` is a command line tool that converts Markdown files into Word
(`.doc`) documents. The tool relies on Pandoc and provides a simple interface
for local documentation workflows.

## Build requirements

- **Python 3.8 or later**
- **Hatch** for packaging and building. Install it using `pip install hatch` or
  `pipx install hatch`.

Runtime dependencies such as `pypandoc-binary` and `pyperclip` are installed
when you install the package.

## Building from source with Hatch

1. Install the build requirements listed above.
2. From the repository root, run:
   ```bash
   hatch build
   ```
   This creates distribution archives inside the `dist/` directory.

## Installing the package

After building, install the generated wheel into your environment:

```bash
pip install dist/md_to_confluence-<version>-py3-none-any.whl
```

For development, you can install the package in editable mode with:

```bash
pip install -e .
```

## Testing

The project uses Ruff for linting, Bandit for security checks and Pytest for
unit tests. After installing these tools, run:

```bash
ruff check .
bandit -r md_to_confluence
pytest tests
```

A successful run shows zero Bandit issues and all tests passing.
