# Copyright (c) 2025 Naren Yellavula & Cybrota contributors
# Apache License, Version 2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
"""Conversion utilities for Markdown to Word documents."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile
import re

import pypandoc
import pyperclip
from pyperclip import PyperclipException


def _set_app_version(docx_file: Path, version: str = "16.0000") -> None:
    """Update ``docProps/app.xml`` ``AppVersion`` to mimic newer Word versions."""

    with ZipFile(docx_file) as zf:
        files = {name: zf.read(name) for name in zf.namelist()}

    app_xml = files.get("docProps/app.xml")
    if not app_xml:
        return

    text = app_xml.decode("utf-8")
    new_text, count = re.subn(
        r"<AppVersion>[^<]*</AppVersion>",
        f"<AppVersion>{version}</AppVersion>",
        text,
        count=1,
    )
    if count:
        files["docProps/app.xml"] = new_text.encode()
        with ZipFile(docx_file, "w") as zf:
            for name, data in files.items():
                zf.writestr(name, data)


def convert(input_path: str | Path, output_path: str | Path) -> Path:
    """Convert markdown file to a Word ``.docx`` document.

    Parameters
    ----------
    input_path: str | Path
        Path to the Markdown file.
    output_path: str | Path
        Where to store the generated Word document.

    Returns
    -------
    Path
        Path to the generated Word document.
    """

    input_file = Path(input_path)
    output_file = Path(output_path)

    text = input_file.read_text()

    # Ensure the pandoc binary is available.
    pypandoc.ensure_pandoc_installed()

    # Convert using pandoc to retain complex entities such as tables.
    pypandoc.convert_text(
        text,
        "docx",
        format="md",
        outputfile=str(output_file),
    )

    # Ensure the file advertises a modern Word version.
    _set_app_version(output_file)

    try:
        pyperclip.copy(str(output_file))
    except PyperclipException:
        # Clipboard support is optional. Continue without failing.
        pass

    return output_file
