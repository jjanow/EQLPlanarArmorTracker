"""Renders armor-completion reports as plain text (no I/O -- see cli.py)."""

from __future__ import annotations

from armor_data import ARMOR_SETS, UNIVERSAL_DROPS, ArmorSet, format_drop_sources


def _pieces_owned(armor_set: ArmorSet, owned: dict[str, int]) -> int:
    return sum(1 for piece in armor_set.pieces if owned.get(piece.name.lower(), 0) >= piece.need)


def _render_set(armor_set: ArmorSet, have: int, total: int, owned: dict[str, int]) -> str:
    lines = [f"\n{armor_set.name} ({armor_set.who}) -- {have}/{total} pieces"]
    for piece in armor_set.pieces:
        count = owned.get(piece.name.lower(), 0)
        mark = "x" if count >= piece.need else " "
        qty = f"{count}/{piece.need}" if piece.need > 1 else ("1" if count else "0")
        line = f"  [{mark}] {piece.slot:<6} {piece.name:<32} {qty}"
        if count < piece.need:
            sources = format_drop_sources(piece.slot, armor_set.group)
            if sources:
                line += f"\n        drops from -- {sources}"
        lines.append(line)
    return "\n".join(lines)


def render_character_report(character: str, owned: dict[str, int]) -> str:
    """Renders the full report for one character as a single text block."""
    chunks = [f"\n{'=' * 70}\n{character}\n{'=' * 70}"]

    complete, partial, empty = [], [], []
    for armor_set in ARMOR_SETS:
        have = _pieces_owned(armor_set, owned)
        total = len(armor_set.pieces)
        (complete if have == total else partial if have else empty).append((armor_set, have, total))

    if complete:
        chunks.append("\n--- COMPLETE SETS ---")
        for armor_set, have, total in sorted(complete, key=lambda r: r[0].name):
            chunks.append(_render_set(armor_set, have, total, owned))

    if partial:
        chunks.append("\n--- IN PROGRESS ---")
        for armor_set, have, total in sorted(partial, key=lambda r: (-r[1], r[0].name)):
            chunks.append(_render_set(armor_set, have, total, owned))

    if empty:
        names = ", ".join(f"{s.name} ({s.who})" for s, _, _ in sorted(empty, key=lambda r: r[0].name))
        chunks.append(f"\n--- NOT STARTED (0 pieces) ---\n  {names}")

    return "\n".join(chunks)


def render_footer() -> str:
    lines = [
        "\nAlso keep an eye out for these rare, universal droppers -- "
        "they can drop any planar class's piece for the slot they hit:"
    ]
    for mob, note in UNIVERSAL_DROPS:
        lines.append(f"  {mob} ({note})")
    return "\n".join(lines)
