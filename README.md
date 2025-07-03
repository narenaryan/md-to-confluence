# md-to-confluence

`md-to-confluence` provides a command line tool that converts Markdown files
into Word (`.docx`) documents. The initial implementation used Python and
Pandoc. A Go based CLI is now available which relies on Pandoc and LibreOffice
for improved compatibility with Confluence imports.

## Build requirements

- **Go 1.21 or later**
- **Python 3.8 or later** (only required for legacy version and tests)
  Runtime dependencies such as `pypandoc-binary` and `pyperclip` are installed
  when you install the Python package.

## Building from source with Hatch

1. Install Go and the other build requirements listed above.
2. Build the Go CLI using:
   ```bash
   go build ./cmd/mdtoconf
   ```
   This produces a binary named `mdtoconf`.
3. The Python package can still be built with Hatch if required.

## Installing the package

After building the Go binary you can install it with `go install` or copy the
binary into your `PATH`. If building the Python package, install the generated
wheel into your environment:

```bash
pip install dist/md_to_confluence-0.1.0-py3-none-any.whl
```

For development, you can install the package in editable mode with:

```bash
pip install -e .
```

## Usage

The project uses Ruff for linting, Bandit for security checks and Pytest for
unit tests. After installing these tools, run:

```bash
mdtoconf -input input.md -output output.docx
```

Now, one can import `output.docx` into Confluence by:

Selecting Three dots (...) -> Templates & Import Doc -> Import -> Microsoft Word & then select "output.docx" from the filesystem.
