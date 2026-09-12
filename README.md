# EQLPlanarArmorTracker

A small command-line tool for **EverQuest Legends** players farming Classic
Planar Armor. Point it at your inventory dumps and it tells you, per
character and per class set, which pieces you already have and which are
still missing -- plus which zone and mobs drop each missing piece.

Every class set is tracked for every character regardless of which class
they're currently playing, since EQ Legends lets you freely switch classes.

Works the same way on **Windows** and **Linux/macOS**.

## Requirements

- Python 3.9 or newer ([python.org](https://www.python.org/downloads/) on
  Windows; usually preinstalled on Linux/macOS, or available via your
  package manager)
- No third-party dependencies

## Getting your inventory data

In-game, run:

```
/outputfile inventory
```

This writes a `<Character>_<Server>-Inventory.txt` dump to your EverQuest
Legends install folder.

## Usage

**Windows:** double-click `run.bat`, or from a terminal (cmd/PowerShell):

```
run.bat                                 # auto-discover *-Inventory.txt dumps
run.bat <path-to-file-or-dir>           # check one dump, or scan a directory
run.bat -o report.txt                   # write the report somewhere other
                                         # than .\eq_planar_armor_report.txt
```

**Linux/macOS:** run `./run.sh`, or call Python directly:

```
./run.sh                                    # auto-discover *-Inventory.txt dumps
python3 eq_planar_armor.py <path-to-file>   # check one specific dump
python3 eq_planar_armor.py <path-to-dir>    # scan every dump in a directory
python3 eq_planar_armor.py -o report.txt    # write the report somewhere other
                                             # than ./eq_planar_armor_report.txt
```

The launcher scripts (`run.bat` / `run.sh`) just find a working Python
interpreter and forward all arguments to `eq_planar_armor.py`; calling
`python`/`python3 eq_planar_armor.py ...` directly works identically on
either OS.

With no arguments, the tool searches common EQ Legends install locations for
`*-Inventory.txt` files:

- **Windows:** `%PUBLIC%\Daybreak Game Company\Installed Games` (and its
  subdirectories), plus `Documents\EverQuest`
- **Linux/macOS:** `~/.wine`, `~/Games`, `~/.local/share/wineprefixes`, and
  any subdirectory of those (Wine prefixes), under
  `drive_c/users/Public/Daybreak Game Company/Installed Games`, plus
  `~/Documents/EverQuest`
- the current directory, on either OS

If your dumps live somewhere else, either pass the path explicitly or set
`EQ_PLANAR_ARMOR_DIR` (or the eqskytracker-compatible `EQSKYTRACKER_DIR`) to
an extra root to search:

```
set EQ_PLANAR_ARMOR_DIR=D:\path\to\dumps        REM cmd
$env:EQ_PLANAR_ARMOR_DIR = "D:\path\to\dumps"   # PowerShell
export EQ_PLANAR_ARMOR_DIR=/path/to/dumps       # bash/zsh
```

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

- **`armor_data.json`** -- the reference data: every armor set, its pieces
  and required quantities, and which mobs/zones drop each slot. Scraped
  from [eqlwiki.com](https://eqlwiki.com/Classic_Planar_Armor:_Group_1). If
  the wiki data changes or you spot an error, this is the only file you
  should need to edit -- the rest of the tool is generic over whatever sets
  are listed here. It's plain JSON (see its `_meta` block for sourcing
  notes and structural gotchas) so it can be reused from other tools or
  projects without depending on any of the Python code below.
- **`armor_data.py`** -- loads `armor_data.json` into typed Python objects.
- **`inventory.py`** -- finds and parses `*-Inventory.txt` dump files.
- **`report.py`** -- turns parsed inventory data into the text report.
- **`eq_planar_armor.py`** -- the command-line entry point that ties the
  above together.
- **`run.sh`** / **`run.bat`** -- launcher scripts for Linux/macOS and
  Windows that find a Python interpreter and run `eq_planar_armor.py`.

## Notes

- Every set has 7 distinct piece names across 8 gear slots: the
  wrist piece (bracer/wristband/etc.) is worn on both wrist slots, so it
  needs a quantity of 2 to count as "complete". Shiverback-hide (Monk) has
  no head-slot piece, so that set completes at 6/6.
- Two rare, universal droppers (a Phoboplasm in Fear, a haunted chest in the
  Hate raid instance) can drop *any* planar class's piece for the slot they
  hit -- these are called out at the end of every report rather than per-set.
