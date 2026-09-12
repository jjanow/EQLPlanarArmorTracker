# EQLPlanarArmorTracker

A small command-line tool for **EverQuest Legends** players farming Classic
Planar Armor. Point it at your inventory dumps and it tells you, per
character and per class set, which pieces you already have and which are
still missing -- plus which zone and mobs drop each missing piece.

Every class set is tracked for every character regardless of which class
they're currently playing, since EQ Legends lets you freely switch classes.

## Requirements

- Python 3.9 or newer
- No third-party dependencies

## Getting your inventory data

In-game, run:

```
/outputfile inventory
```

This writes a `<Character>_<Server>-Inventory.txt` dump to your EverQuest
Legends install folder.

## Usage

```
python3 eq_planar_armor.py                  # auto-discover *-Inventory.txt dumps
python3 eq_planar_armor.py <path-to-file>    # check one specific dump
python3 eq_planar_armor.py <path-to-dir>     # scan every dump in a directory
python3 eq_planar_armor.py -o report.txt     # write the report somewhere other
                                              # than ./eq_planar_armor_report.txt
```

With no arguments, the tool searches common EQ Legends install locations for
`*-Inventory.txt` files:

- `~/.wine`, `~/Games`, `~/.local/share/wineprefixes`, and any subdirectory
  of those (Wine prefixes), under
  `drive_c/users/Public/Daybreak Game Company/Installed Games`
- `~/Documents/EverQuest`
- the current directory

If your dumps live somewhere else, either pass the path explicitly or set
`EQ_PLANAR_ARMOR_DIR` (or the eqskytracker-compatible `EQSKYTRACKER_DIR`) to
an extra root to search.

The report is printed to the terminal and also saved to
`eq_planar_armor_report.txt` (or wherever `-o`/`--output` points).

### Sample output

```
======================================================================
Grimtooth_Rivervale
======================================================================

--- COMPLETE SETS ---

Valorium Armor (Paladin) -- 7/7 pieces
  [x] Head   Valorium Helmet                  1
  [x] Chest  Valorium Chestplate              1
  [x] Arms   Valorium Vambraces               1
  [x] Wrist  Valorium Bracer                  2/2
  [x] Hands  Valorium Gauntlets               1
  [x] Legs   Valorium Greaves                 1
  [x] Feet   Valorium Boots                   1

--- IN PROGRESS ---

Ethereal Mist Armor (Cleric) -- 3/7 pieces
  [x] Head   Ethereal Mist Helm               1
  [ ] Chest  Ethereal Mist Chestplate         0
        drops from -- Fear: a glare lord, a tentacle tormentor
  ...

--- NOT STARTED (0 pieces) ---
  Apothic Armor (Magician), Blighted Armor (Necromancer), ...
```

## How the data is organized

- **`armor_data.py`** -- the reference data: every armor set, its pieces and
  required quantities, and which mobs/zones drop each slot. Scraped from
  [eqlwiki.com](https://eqlwiki.com/Classic_Planar_Armor:_Group_1). If the
  wiki data changes or you spot an error, this is the only file you should
  need to edit -- the rest of the tool is generic over whatever sets are
  listed here.
- **`inventory.py`** -- finds and parses `*-Inventory.txt` dump files.
- **`report.py`** -- turns parsed inventory data into the text report.
- **`eq_planar_armor.py`** -- the command-line entry point that ties the
  above together.

## Notes

- Every set has 7 distinct piece names across 8 gear slots: the
  wrist piece (bracer/wristband/etc.) is worn on both wrist slots, so it
  needs a quantity of 2 to count as "complete". Shiverback-hide (Monk) has
  no head-slot piece, so that set completes at 6/6.
- Two rare, universal droppers (a Phoboplasm in Fear, a haunted chest in the
  Hate raid instance) can drop *any* planar class's piece for the slot they
  hit -- these are called out at the end of every report rather than per-set.
