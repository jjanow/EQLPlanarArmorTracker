#!/usr/bin/env python3
"""
Report which Classic Planar Armor pieces you own vs. still need, across every
class set (Group 1 + Group 2, https://eqlwiki.com/Classic_Planar_Armor:_Group_1
and _Group_2) plus the two generic sets (Lustrous Russet for plate/chain,
Midnight Clad for leather/cloth). Every class is tracked regardless of which
one you're currently playing, since EQ Legends lets you switch classes.

Reads EverQuest-style "/outputfile inventory" dumps
(<Character>_<Server>-Inventory.txt); see inventory.py for the file format
and auto-discovery locations, and armor_data.json for the set/drop data
(armor_data.py just loads it).

Works the same on Windows and Linux/macOS -- run it with `python` or
`python3` directly, or use run.bat (Windows) / run.sh (Linux/macOS).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from inventory import find_inventory_files, parse_inventory
from report import render_character_report, render_footer

DEFAULT_OUTPUT_FILENAME = "eq_planar_armor_report.txt"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report owned vs. missing Classic Planar Armor pieces from EQ inventory dumps.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="a specific *-Inventory.txt dump, or a directory to scan. "
        "Omit to auto-discover dumps in common EQ Legends install locations.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_OUTPUT_FILENAME,
        help=f"where to write the report (default: {DEFAULT_OUTPUT_FILENAME} in the current directory)",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args(sys.argv[1:])
    files = find_inventory_files(args.path)
    if not files:
        print("No *-Inventory.txt dump files found. Run '/outputfile inventory' in-game,")
        print("or pass a path: python3 eq_planar_armor.py <file-or-directory>")
        sys.exit(1)

    chunks = []
    for f in files:
        character = f.name.removesuffix("-Inventory.txt")
        owned = parse_inventory(f)
        chunks.append(render_character_report(character, owned))
    chunks.append(render_footer())
    text = "\n".join(chunks) + "\n"

    out_path = Path(args.output)
    out_path.write_text(text, encoding="utf-8")
    print(text, end="")
    print(f"\nReport written to {out_path.resolve()}")


if __name__ == "__main__":
    main()
