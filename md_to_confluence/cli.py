# Copyright (c) 2025 Naren Yellavula & Cybrota contributors
# Apache License, Version 2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
"""Command line interface for the md-to-confluence package."""

from __future__ import annotations

import argparse
from pathlib import Path

from .converter import convert


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert Markdown to a Word .doc file")
    parser.add_argument("input", type=Path, help="Markdown file")
    parser.add_argument("output", type=Path, help="Output .doc file")

    args = parser.parse_args(argv)

    convert(args.input, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
