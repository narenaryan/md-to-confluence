# Copyright (c) 2025 Naren Yellavula & Cybrota contributors
# Apache License, Version 2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

import pyperclip

import md_to_confluence.converter as conv


def test_convert(tmp_path, monkeypatch):
    md_text = "# Title"
    input_file = tmp_path / "test.md"
    output_file = tmp_path / "out.txt"
    input_file.write_text(md_text)

    monkeypatch.setattr(pyperclip, "copy", lambda text: None)
    monkeypatch.setattr(conv.pypandoc, "convert_text", lambda *a, **k: "h1. Title")

    result = conv.convert(input_file, output_file)

    assert output_file.read_text() == "h1. Title"
    assert result == "h1. Title"
