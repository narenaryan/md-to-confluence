# Copyright (c) 2025 Naren Yellavula & Cybrota contributors
# Apache License, Version 2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
"""Conversion utilities for Markdown to Word documents."""

from __future__ import annotations

from pathlib import Path

import pypandoc
import pyperclip
from pyperclip import PyperclipException


def convert(input_path: str | Path, output_path: str | Path) -> Path:
    """Convert markdown file to a Word ``.doc`` document.

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
        "doc",
        format="md",
        outputfile=str(output_file),
    )

    try:
        pyperclip.copy(str(output_file))
    except PyperclipException:
        # Clipboard support is optional. Continue without failing.
        pass

    return output_file
