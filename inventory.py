"""
Discovery and parsing of EverQuest-style "/outputfile inventory" dumps
(<Character>_<Server>-Inventory.txt).

This mirrors the same format and discovery locations eqskytracker's
Inventory.cs / Discovery.cs use:
  https://github.com/.../eqskytracker/blob/main/src/EqSkyTracker.Core/Inventory.cs
  https://github.com/.../eqskytracker/blob/main/src/EqSkyTracker.Core/Discovery.cs
"""

from __future__ import annotations

import json
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

# Caches the directories found by find_candidate_dirs() so repeat runs don't
# have to re-walk Wine prefixes / Installed Games trees every time. Plain
# JSON, safe to hand-edit -- add or remove paths under "discovered_dirs" and
# they'll be used as-is on the next run, no rescan needed.
CONFIG_FILE = Path(__file__).resolve().parent / "eq_planar_armor_config.json"


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


def load_config_dirs() -> list[Path]:
    """Returns the cached directory list from CONFIG_FILE, or [] if missing/invalid."""
    try:
        raw = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return [Path(p) for p in raw.get("discovered_dirs", [])]


def save_config_dirs(dirs: list[Path]) -> None:
    paths = sorted({str(d.resolve()) for d in dirs})
    payload = {
        "_comment": (
            "Cached EQ Legends install/dump directories, so eq_planar_armor.py "
            "doesn't have to re-scan Wine prefixes and Installed Games trees on "
            "every run. Feel free to hand-edit 'discovered_dirs' -- add, remove, "
            "or fix a path -- or just delete this file / pass --rescan to have "
            "it regenerated from scratch."
        ),
        "discovered_dirs": paths,
    }
    CONFIG_FILE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def add_config_dir(path: Path) -> list[Path]:
    """Adds one directory to the cached list (creating it if needed) and saves it."""
    dirs = [d for d in load_config_dirs() if d.is_dir()]
    dirs.append(path)
    save_config_dirs(dirs)
    return dirs


def get_search_dirs(rescan: bool = False) -> list[Path]:
    """Returns the directories to search for inventory dumps, using the cached
    config unless it's missing, empty, stale (no surviving dirs), or a rescan
    is requested -- in which case it re-discovers and re-caches them."""
    if not rescan:
        cached = [d for d in load_config_dirs() if d.is_dir()]
        if cached:
            return cached

    discovered = find_candidate_dirs()
    save_config_dirs(discovered)
    return discovered


def find_candidate_dirs() -> list[Path]:
    home = Path.home()
    env_dir = next((os.environ[v] for v in _DIR_OVERRIDE_ENV_VARS if os.environ.get(v)), None)
    roots = [Path(env_dir)] if env_dir else []

    # Linux/macOS: the game runs inside a Wine prefix, which simulates a
    # Windows filesystem rooted at <prefix>/drive_c.
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

    # Native Windows: same relative layout, rooted at the real Public
    # profile. %PUBLIC% is set by Windows itself; fall back to the
    # conventional path if it's missing (e.g. a non-standard shell).
    public_dir = Path(os.environ.get("PUBLIC", r"C:\Users\Public"))
    installed_games = public_dir / "Daybreak Game Company/Installed Games"
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


def find_inventory_files(arg: str | None, rescan: bool = False) -> list[Path]:
    if arg:
        p = Path(arg).expanduser()
        if p.is_file():
            return [p]
        if p.is_dir():
            return sorted(p.glob("*-Inventory.txt"))
        print(f"error: path not found: {p}", file=sys.stderr)
        sys.exit(1)

    found: dict[str, Path] = {}
    for d in get_search_dirs(rescan=rescan):
        for f in d.glob("*-Inventory.txt"):
            found.setdefault(f.name, f)
    return sorted(found.values())
