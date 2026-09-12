"""
Classic Planar Armor set and drop data, scraped from eqlwiki.

Sources:
  Group overviews:  https://eqlwiki.com/Classic_Planar_Armor:_Group_1
                     https://eqlwiki.com/Classic_Planar_Armor:_Group_2
  Per-set pages linked off those two, e.g.:
                     https://eqlwiki.com/Ethereal_Mist_Armor
                     https://eqlwiki.com/Midnight_Clad_Armor

Every class set (Group 1 + Group 2) plus the two generic sets (Lustrous
Russet for plate/chain, Midnight Clad for leather/cloth) is tracked here,
regardless of which class you're currently playing, since EQ Legends lets
you switch classes freely.

To correct or extend this data (e.g. a wiki update, a set that changed),
edit ARMOR_SETS / GROUP_DROPS / UNIVERSAL_DROPS below -- eq_planar_armor.py
itself never needs to change for a data-only update.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

WRIST = "Wrist"


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


# ---------------------------------------------------------------------------
# Every set has 7 distinct piece *names* but 8 slots -- the wrist bracer/
# wristband/etc. is worn on both wrist slots, so it needs a quantity of 2 to
# be "complete". Shiverback-hide (Monk) has no head piece, so its set is
# complete at 6/6.
# ---------------------------------------------------------------------------

ARMOR_SETS: list[ArmorSet] = [
    ArmorSet(
        "Lustrous Russet Armor",
        "Generic (Plate/Chain)",
        1,
        [
            ArmorPiece("Head", "Lustrous Russet Helm"),
            ArmorPiece("Chest", "Lustrous Russet Breastplate"),
            ArmorPiece("Arms", "Lustrous Russet Vambraces"),
            ArmorPiece(WRIST, "Lustrous Russet Bracer", 2),
            ArmorPiece("Hands", "Lustrous Russet Gauntlets"),
            ArmorPiece("Legs", "Lustrous Russet Greaves"),
            ArmorPiece("Feet", "Lustrous Russet Boots"),
        ],
    ),
    ArmorSet(
        "Midnight Clad Armor",
        "Generic (Leather/Cloth)",
        2,
        [
            ArmorPiece("Head", "Midnight Clad Headband"),
            ArmorPiece("Chest", "Midnight Clad Straps"),
            ArmorPiece("Arms", "Midnight Clad Armbands"),
            ArmorPiece(WRIST, "Midnight Clad Wristbands", 2),
            ArmorPiece("Hands", "Midnight Clad Fistwraps"),
            ArmorPiece("Legs", "Midnight Clad Leggings"),
            ArmorPiece("Feet", "Midnight Clad Footwraps"),
        ],
    ),
    ArmorSet(
        "Anthemion Armor",
        "Beastlord",
        1,
        [
            ArmorPiece("Head", "Anthemion Skullcap"),
            ArmorPiece("Chest", "Anthemion Jerkin"),
            ArmorPiece("Arms", "Anthemion Armbands"),
            ArmorPiece(WRIST, "Anthemion Wristguard", 2),
            ArmorPiece("Hands", "Anthemion Gloves"),
            ArmorPiece("Legs", "Anthemion Leggings"),
            ArmorPiece("Feet", "Anthemion Boots"),
        ],
    ),
    ArmorSet(
        "Imbrued Armor",
        "Bard",
        2,
        [
            ArmorPiece("Head", "Imbrued Platemail Helm"),
            ArmorPiece("Chest", "Imbrued Platemail Breastplate"),
            ArmorPiece("Arms", "Imbrued Platemail Vambraces"),
            ArmorPiece(WRIST, "Imbrued Platemail Bracer", 2),
            ArmorPiece("Hands", "Imbrued Platemail Gauntlets"),
            ArmorPiece("Legs", "Imbrued Platemail Greaves"),
            ArmorPiece("Feet", "Imbrued Platemail Boots"),
        ],
    ),
    ArmorSet(
        "Shadow Rage Armor",
        "Berserker",
        1,
        [
            ArmorPiece("Head", "Shadow Rage Helm"),
            ArmorPiece("Chest", "Shadow Rage Tunic"),
            ArmorPiece("Arms", "Shadow Rage Sleeves"),
            ArmorPiece(WRIST, "Shadow Rage Wristguard", 2),
            ArmorPiece("Hands", "Shadow Rage Gloves"),
            ArmorPiece("Legs", "Shadow Rage Leggings"),
            ArmorPiece("Feet", "Shadow Rage Boots"),
        ],
    ),
    ArmorSet(
        "Insidious Armor",
        "Enchanter",
        2,
        [
            ArmorPiece("Head", "Insidious Halo"),
            ArmorPiece("Chest", "Insidious Robe"),
            ArmorPiece("Arms", "Insidious Sleeves"),
            ArmorPiece(WRIST, "Insidious Manacle", 2),
            ArmorPiece("Hands", "Insidious Gloves"),
            ArmorPiece("Legs", "Insidious Pantaloons"),
            ArmorPiece("Feet", "Insidious Slippers"),
        ],
    ),
    ArmorSet(
        "Ethereal Mist Armor",
        "Cleric",
        1,
        [
            ArmorPiece("Head", "Ethereal Mist Helm"),
            ArmorPiece("Chest", "Ethereal Mist Chestplate"),
            ArmorPiece("Arms", "Ethereal Mist Vambraces"),
            ArmorPiece(WRIST, "Ethereal Mist Bracers", 2),
            ArmorPiece("Hands", "Ethereal Mist Gauntlets"),
            ArmorPiece("Legs", "Ethereal Mist Greaves"),
            ArmorPiece("Feet", "Ethereal Mist Boots"),
        ],
    ),
    ArmorSet(
        "Apothic Armor",
        "Magician",
        2,
        [
            ArmorPiece("Head", "Apothic Crown"),
            ArmorPiece("Chest", "Apothic Robe"),
            ArmorPiece("Arms", "Apothic Sleeves"),
            ArmorPiece(WRIST, "Apothic Warband", 2),
            ArmorPiece("Hands", "Apothic Gloves"),
            ArmorPiece("Legs", "Apothic Kilt"),
            ArmorPiece("Feet", "Apothic Boots"),
        ],
    ),
    ArmorSet(
        "Vermiculated Armor",
        "Druid",
        1,
        [
            ArmorPiece("Head", "Vermiculated Crown"),
            ArmorPiece("Chest", "Vermiculated Tunic"),
            ArmorPiece("Arms", "Vermiculated Armplates"),
            ArmorPiece(WRIST, "Vermiculated Bracelet", 2),
            ArmorPiece("Hands", "Vermiculated Gloves"),
            ArmorPiece("Legs", "Vermiculated Leggings"),
            ArmorPiece("Feet", "Vermiculated Boots"),
        ],
    ),
    ArmorSet(
        "Blighted Armor",
        "Necromancer",
        2,
        [
            ArmorPiece("Head", "Blighted Skullcap"),
            ArmorPiece("Chest", "Blighted Robe"),
            ArmorPiece("Arms", "Blighted Sleeves"),
            ArmorPiece(WRIST, "Blighted Armband", 2),
            ArmorPiece("Hands", "Blighted Gloves"),
            ArmorPiece("Legs", "Blighted Trousers"),
            ArmorPiece("Feet", "Blighted Boots"),
        ],
    ),
    ArmorSet(
        "Shiverback-hide Armor",
        "Monk",
        1,
        [
            # No head-slot piece exists for this set.
            ArmorPiece("Chest", "Shiverback-hide Jerkin"),
            ArmorPiece("Arms", "Shiverback-hide Armbands"),
            ArmorPiece(WRIST, "Shiverback-hide Wristbands", 2),
            ArmorPiece("Hands", "Shiverback-hide Gloves"),
            ArmorPiece("Legs", "Shiverback-hide Leggings"),
            ArmorPiece("Feet", "Shiverback-hide Boots"),
        ],
    ),
    ArmorSet(
        "Woven Shadow Armor",
        "Rogue",
        2,
        [
            ArmorPiece("Head", "Woven Shadow Helm"),
            ArmorPiece("Chest", "Woven Shadow Chestplate"),
            ArmorPiece("Arms", "Woven Shadow Vambraces"),
            ArmorPiece(WRIST, "Woven Shadow Bracer", 2),
            ArmorPiece("Hands", "Woven Shadow Gauntlets"),
            ArmorPiece("Legs", "Woven Shadow Greaves"),
            ArmorPiece("Feet", "Woven Shadow Boots"),
        ],
    ),
    ArmorSet(
        "Valorium Armor",
        "Paladin",
        1,
        [
            ArmorPiece("Head", "Valorium Helmet"),
            ArmorPiece("Chest", "Valorium Chestplate"),
            ArmorPiece("Arms", "Valorium Vambraces"),
            ArmorPiece(WRIST, "Valorium Bracer", 2),
            ArmorPiece("Hands", "Valorium Gauntlets"),
            ArmorPiece("Legs", "Valorium Greaves"),
            ArmorPiece("Feet", "Valorium Boots"),
        ],
    ),
    ArmorSet(
        "Umbral Platemail",
        "Shadow Knight",
        2,
        [
            ArmorPiece("Head", "Umbral Platemail Helm"),
            ArmorPiece("Chest", "Umbral Platemail Breastplate"),
            ArmorPiece("Arms", "Umbral Platemail Vambraces"),
            ArmorPiece(WRIST, "Umbral Platemail Bracer", 2),
            ArmorPiece("Hands", "Umbral Platemail Gauntlets"),
            ArmorPiece("Legs", "Umbral Platemail Greaves"),
            ArmorPiece("Feet", "Umbral Platemail Boots"),
        ],
    ),
    ArmorSet(
        "Thorny Vine Armor",
        "Ranger",
        1,
        [
            ArmorPiece("Head", "Thorny Vine Helm"),
            ArmorPiece("Chest", "Thorny Vine Chestplate"),
            ArmorPiece("Arms", "Thorny Vine Vambraces"),
            ArmorPiece(WRIST, "Thorny Vine Bracer", 2),
            ArmorPiece("Hands", "Thorny Vine Gauntlets"),
            ArmorPiece("Legs", "Thorny Vine Greaves"),
            ArmorPiece("Feet", "Thorny Vine Boots"),
        ],
    ),
    ArmorSet(
        "Indicolite Armor",
        "Warrior",
        2,
        [
            ArmorPiece("Head", "Indicolite Helm"),
            ArmorPiece("Chest", "Indicolite Breastplate"),
            ArmorPiece("Arms", "Indicolite Vambraces"),
            ArmorPiece(WRIST, "Indicolite Bracer", 2),
            ArmorPiece("Hands", "Indicolite Gauntlets"),
            ArmorPiece("Legs", "Indicolite Greaves"),
            ArmorPiece("Feet", "Indicolite Boots"),
        ],
    ),
    ArmorSet(
        "Rune Etched Armor",
        "Shaman",
        1,
        [
            ArmorPiece("Head", "Rune Etched Helm"),
            ArmorPiece("Chest", "Rune Etched Chestplate"),
            ArmorPiece("Arms", "Rune Etched Vambraces"),
            ArmorPiece(WRIST, "Rune Etched Bracer", 2),
            ArmorPiece("Hands", "Rune Etched Gauntlets"),
            ArmorPiece("Legs", "Rune Etched Greaves"),
            ArmorPiece("Feet", "Rune Etched Boots"),
        ],
    ),
    ArmorSet(
        "Carmine Armor",
        "Wizard",
        2,
        [
            ArmorPiece("Head", "Carmine Turban"),
            ArmorPiece("Chest", "Carmine Robe"),
            ArmorPiece("Arms", "Carmine Sleeves"),
            ArmorPiece(WRIST, "Carmine Trinket", 2),
            ArmorPiece("Hands", "Carmine Gloves"),
            ArmorPiece("Legs", "Carmine Pants"),
            ArmorPiece("Feet", "Carmine Boots"),
        ],
    ),
]

# ---------------------------------------------------------------------------
# Who drops the missing pieces, scraped from the raw "Group 1 Mobs" /
# "Group 2 Mobs" tables on https://eqlwiki.com/Classic_Planar_Armor:_Group_1
# and _Group_2 (each armor set belongs to one of those two groups; every mob
# in a group can drop any set's piece for the matching slot). Chest/Hands/
# Feet/Wrist drop in the Plane of Fear; Arms/Head/Legs/Wrist drop in the
# Plane of Hate -- Wrist needs 2 and can come from either zone's mobs.
# ---------------------------------------------------------------------------

GROUP_DROPS: dict[int, dict[str, list[tuple[str, str]]]] = {
    1: {
        "Chest": [("a glare lord", "Fear"), ("a tentacle tormentor", "Fear")],
        "Hands": [("a scareling", "Fear"), ("a shiverback", "Fear")],
        "Feet": [("a boogeyman", "Fear"), ("a phantasm", "Fear")],
        WRIST: [
            ("a decrepit warder", "Fear"),
            ("a samhain", "Fear"),
            ("an abhorrent", "Hate"),
            ("a scorn banshee", "Hate"),
        ],
        "Arms": [("a forsaken revenant (female)", "Hate"), ("an ire ghast", "Hate")],
        "Head": [("Cleric of Innoruuk", "Hate")],
        "Legs": [
            ("an elite dragoon (male)", "Hate"),
            ("Innoruuk's Chosen (male)", "Hate"),
            ("a Disciple of Innoruuk", "Hate"),
            ("a Knight of Innoruuk", "Hate"),
        ],
    },
    2: {
        "Chest": [("amygdalan knight", "Fear"), ("amygdalan warrior", "Fear")],
        "Hands": [
            ("a frightfinger", "Fear"),
            ("a turmoil toad", "Fear"),
            ("a worry wraith", "Fear"),
        ],
        "Feet": [("a gorgon", "Fear"), ("a nightmare", "Fear")],
        WRIST: [
            ("a fetid fiend", "Fear"),
            ("a spinechiller spider", "Fear"),
            ("a kiraikuei", "Hate"),
            ("a loathling lich", "Hate"),
            ("a revultant rat", "Hate"),
        ],
        "Arms": [("a forsaken revenant (male)", "Hate"), ("an ashenbone drake", "Hate")],
        "Head": [("a spite golem", "Hate")],
        "Legs": [
            ("an elite dragoon (female)", "Hate"),
            ("Innoruuk's Chosen (female)", "Hate"),
            ("an Agent of Innoruuk", "Hate"),
            ("a Champion of Innoruuk", "Hate"),
            ("a Sage of Innoruuk", "Hate"),
        ],
    },
}

# A pair of rare, universal droppers noted on the per-set eqlwiki pages
# (e.g. https://eqlwiki.com/Ethereal_Mist_Armor, https://eqlwiki.com/Midnight_Clad_Armor):
# these can drop *any* planar class's piece for the slot they hit, on top of
# the group-specific mobs above.
UNIVERSAL_DROPS: list[tuple[str, str]] = [
    ("Phoboplasm", "Plane of Fear -- rare, any slot/set"),
    ("A haunted chest (Innoruuk raid instance)", "Plane of Hate -- rare, any slot/set"),
]


def format_drop_sources(slot: str, group: int) -> str:
    entries = GROUP_DROPS.get(group, {}).get(slot, [])
    by_zone: dict[str, list[str]] = defaultdict(list)
    for mob, zone in entries:
        by_zone[zone].append(mob)
    return "; ".join(f"{zone}: {', '.join(mobs)}" for zone, mobs in by_zone.items())
