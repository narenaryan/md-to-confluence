# Copyright (c) 2025 Naren Yellavula & Cybrota contributors
# Apache License, Version 2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

import pyperclip
from pathlib import Path
import zipfile

import md_to_confluence.converter as conv


def test_convert(tmp_path, monkeypatch):
    md_text = "# Title"
    input_file = tmp_path / "test.md"
    output_file = tmp_path / "out.doc"
    input_file.write_text(md_text)

    monkeypatch.setattr(pyperclip, "copy", lambda text: None)

    def fake_convert_text(*args, **kwargs):
        with zipfile.ZipFile(Path(kwargs["outputfile"]), "w") as zf:
            zf.writestr(
                "docProps/app.xml",
                "<Properties><AppVersion>12.0000</AppVersion></Properties>",
            )
            zf.writestr("word/document.xml", "<w:document/>")
        return ""

    monkeypatch.setattr(conv.pypandoc, "ensure_pandoc_installed", lambda: None)

    monkeypatch.setattr(conv.pypandoc, "convert_text", fake_convert_text)

    result = conv.convert(input_file, output_file)

    with zipfile.ZipFile(output_file) as zf:
        data = zf.read("docProps/app.xml").decode()
    assert "<AppVersion>16.0000</AppVersion>" in data
    assert result == output_file
