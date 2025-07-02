# Copyright (c) 2025 Naren Yellavula & Cybrota contributors
# Apache License, Version 2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
"""Conversion utilities for Markdown to Confluence."""

from __future__ import annotations

from pathlib import Path

import pypandoc
import pyperclip
from pyperclip import PyperclipException


def convert(input_path: str | Path, output_path: str | Path) -> str:
    """Convert markdown file to Confluence wiki markup.

    Parameters
    ----------
    input_path: str | Path
        Path to the Markdown file.
    output_path: str | Path
        Where to store the generated Confluence markup.

    Returns
    -------
    str
        The generated markup as a string.
    """

    input_file = Path(input_path)
    output_file = Path(output_path)

    text = input_file.read_text()

    # Convert using pandoc. The 'jira' format matches Confluence wiki markup.
    confluence_text = pypandoc.convert_text(text, "jira", format="md")

    try:
        pyperclip.copy(confluence_text)
    except PyperclipException:
        # Clipboard support is optional. Continue without failing.
        pass

    output_file.write_text(confluence_text)
    return confluence_text
