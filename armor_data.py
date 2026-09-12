"""
Loads Classic Planar Armor set and drop data from armor_data.json.

The set/drop data itself lives in armor_data.json (not here) so it can be
reused from other tools/languages without importing this project. This
module just loads it into typed, validated Python objects for the rest of
the tracker to use.

To correct or extend the data (e.g. a wiki update, a set that changed),
edit armor_data.json -- eq_planar_armor.py and this module never need to
change for a data-only update. See the "_meta" block at the top of that
file for sourcing notes and structural gotchas (wrist quantities, drop
zones, etc.).
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "armor_data.json"


@dataclass(frozen=True)
class ArmorPiece:
    slot: str
    name: str
    need: int = 1


@dataclass(frozen=True)
class ArmorSet:
    name: str
    who: str
    group: int
    pieces: list[ArmorPiece] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def _load(path: Path) -> tuple[list[ArmorSet], dict[int, dict[str, list[tuple[str, str]]]], list[tuple[str, str]]]:
    raw = json.loads(path.read_text(encoding="utf-8"))

    armor_sets = [
        ArmorSet(
            name=s["name"],
            who=s["who"],
            group=s["group"],
            pieces=[ArmorPiece(p["slot"], p["name"], p.get("need", 1)) for p in s["pieces"]],
            notes=s.get("notes", []),
        )
        for s in raw["armor_sets"]
    ]
    group_drops = {
        int(group): {slot: [tuple(entry) for entry in entries] for slot, entries in slots.items()}
        for group, slots in raw["group_drops"].items()
    }
    universal_drops = [tuple(entry) for entry in raw["universal_drops"]]
    return armor_sets, group_drops, universal_drops


ARMOR_SETS, GROUP_DROPS, UNIVERSAL_DROPS = _load(DATA_FILE)


def format_drop_sources(slot: str, group: int) -> str:
    entries = GROUP_DROPS.get(group, {}).get(slot, [])
    by_zone: dict[str, list[str]] = defaultdict(list)
    for mob, zone in entries:
        by_zone[zone].append(mob)
    return "; ".join(f"{zone}: {', '.join(mobs)}" for zone, mobs in by_zone.items())
