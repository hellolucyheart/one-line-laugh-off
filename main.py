#!/usr/bin/env python3
"""One-Line Laugh-Off — a single joke, written to /output/entry.txt.

The joke is one sentence, short enough to land cold: a smart speaker
asked for something relaxing answers with the one thing nobody finds
relaxing. No setup, no explanation, just the line.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

JOKE = "I asked my smart speaker for something relaxing, and it read my bank balance out loud."

DEFAULT_DESTINATION = Path("/output/entry.txt")
DESTINATION = Path(os.environ.get("MAKEFUN_OUTPUT", str(DEFAULT_DESTINATION)))
LIMIT = 200


def ensure_single_line(text: str) -> str:
    """Keep only a joke the gate accepts, or stop with a clear error."""
    cleaned = text.strip()
    if not cleaned:
        raise SystemExit("refusing to write an empty entry")
    if len(cleaned) > LIMIT:
        raise SystemExit(f"entry is {len(cleaned)} characters, over the {LIMIT} limit")
    if any(mark in cleaned for mark in ("\n", "\r")):
        raise SystemExit("entry must fit on one line")
    if any(ord(ch) < 32 for ch in cleaned):
        raise SystemExit("entry must not hold control characters")
    if cleaned.count(".") != 1 or not cleaned.endswith("."):
        raise SystemExit("entry must be exactly one sentence")
    return cleaned


def run() -> int:
    line = ensure_single_line(JOKE)
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(line, encoding="utf-8", newline="\n")
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(run())
