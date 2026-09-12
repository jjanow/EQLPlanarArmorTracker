"""
Discovery and parsing of EverQuest-style "/outputfile inventory" dumps
(<Character>_<Server>-Inventory.txt).

This mirrors the same format and discovery locations eqskytracker's
Inventory.cs / Discovery.cs use:
  https://github.com/.../eqskytracker/blob/main/src/EqSkyTracker.Core/Inventory.cs
  https://github.com/.../eqskytracker/blob/main/src/EqSkyTracker.Core/Discovery.cs
"""

from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

_SUFFIX_RE = re.compile(r"\s*(\+\d+|\(Exaltation\))\s*$")

# eqskytracker calls its equivalent search-root override EQSKYTRACKER_DIR;
# EQ_PLANAR_ARMOR_DIR is accepted as an alias since this tool isn't
# eqskytracker, but either name works.
_DIR_OVERRIDE_ENV_VARS = ("EQ_PLANAR_ARMOR_DIR", "EQSKYTRACKER_DIR")


def normalize_item_name(name: str) -> str:
    """Strips trailing "+N" and "(Exaltation)" augment/upgrade suffixes."""
    prev = None
    while prev != name:
        prev = name
        name = _SUFFIX_RE.sub("", name).strip()
    return name


def read_dump_lines(path: Path) -> list[str]:
    raw = path.read_bytes()
    body = raw[3:] if raw[:3] == b"\xef\xbb\xbf" else raw
    text = body.decode("latin-1", errors="replace")
    for encoding in ("utf-8", "cp1252"):
        try:
            text = body.decode(encoding, errors="strict")
            break
        except UnicodeDecodeError:
            continue
    return [line.rstrip("\r") for line in text.split("\n")]


def parse_inventory(path: Path) -> dict[str, int]:
    """Returns normalized item name (lowercased) -> total count owned."""
    lines = read_dump_lines(path)

    owned: dict[str, int] = defaultdict(int)
    for line in lines:
        parts = line.split("\t")
        if not parts or parts[0] in ("Location", "KeyRing", ""):
            continue
        if len(parts) >= 5:
            # Bag/bank/worn slot row: Location, Name, ID, Count, Slots.
            name, item_id, count_raw, slots_raw = parts[1:5]
            if name == "Empty":
                continue
            try:
                int(item_id)
                count = int(count_raw)
                int(slots_raw)
            except ValueError:
                continue
        elif len(parts) == 3:
            # Category-tab row (Equipment/KeyRing/Augmentation/...): no
            # Count/Slots columns -- a single, non-stacking item.
            name, item_id = parts[1], parts[2]
            if name == "Empty":
                continue
            try:
                int(item_id)
            except ValueError:
                continue
            count = 1
        else:
            continue
        owned[normalize_item_name(name).lower()] += count
    return owned


def find_candidate_dirs() -> list[Path]:
    home = Path.home()
    env_dir = next((os.environ[v] for v in _DIR_OVERRIDE_ENV_VARS if os.environ.get(v)), None)
    roots = [Path(env_dir)] if env_dir else []
    wine_root_parents = [home / ".wine", home / "Games", home / ".local/share/wineprefixes"]
    prefixes: list[Path] = []
    for parent in wine_root_parents:
        prefixes.append(parent)
        if parent.is_dir():
            prefixes.extend(p for p in parent.iterdir() if p.is_dir())
    for prefix in prefixes:
        installed_games = prefix / "drive_c/users/Public/Daybreak Game Company/Installed Games"
        if installed_games.is_dir():
            roots.append(installed_games)
            roots.extend(p for p in installed_games.iterdir() if p.is_dir())
    roots.append(home / "Documents/EverQuest")
    roots.append(Path.cwd())

    seen: set[Path] = set()
    unique: list[Path] = []
    for r in roots:
        try:
            resolved = r.resolve()
        except OSError:
            continue
        if resolved not in seen and resolved.is_dir():
            seen.add(resolved)
            unique.append(resolved)
    return unique


def find_inventory_files(arg: str | None) -> list[Path]:
    if arg:
        p = Path(arg).expanduser()
        if p.is_file():
            return [p]
        if p.is_dir():
            return sorted(p.glob("*-Inventory.txt"))
        print(f"error: path not found: {p}", file=sys.stderr)
        sys.exit(1)

    found: dict[str, Path] = {}
    for d in find_candidate_dirs():
        for f in d.glob("*-Inventory.txt"):
            found.setdefault(f.name, f)
    return sorted(found.values())
