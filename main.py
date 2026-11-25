"""Best Meal You Ever Had — one-sentence entry writer.

Writes a single sentence (at most 200 characters) about the best meal
ever had to $MAKEFUN_OUTPUT_DIR/entry.txt (falling back to /output),
then reads it back and validates it: UTF-8, 1-200 chars, one line,
not only whitespace, exactly one sentence.
"""

import os
import sys

ENTRY = (
    "At dusk in my grandmother's kitchen, steam rising off hand-pulled "
    "noodles in rich pork broth, my grandfather slid me the last glistening "
    "piece of braised pork while she pretended not to notice."
)

MAX_CHARS = 200


def validate(text: str) -> None:
    if not text or not text.strip():
        raise SystemExit("entry is empty or only whitespace")
    if len(text) != len(text.strip()):
        raise SystemExit("entry has leading or trailing whitespace")
    if len(text) > MAX_CHARS:
        raise SystemExit(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")
    if "\t" in text or "  " in text:
        raise SystemExit("entry must not contain tabs or double spaces")
    if text.count(".") != 1 or not text.endswith("."):
        raise SystemExit("entry must be exactly one sentence ending in a period")
    words = text.split()
    if len(words) < 10:
        raise SystemExit("entry is too short to feel like a real meal memory")


def main() -> None:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Read-back check: what landed on disk must be byte-identical.
    with open(path, "r", encoding="utf-8", newline="") as f:
        on_disk = f.read()
    if on_disk != ENTRY:
        raise SystemExit("read-back mismatch: entry.txt differs from ENTRY")
    validate(on_disk)
    print(f"wrote {len(on_disk)} chars to {path}")


if __name__ == "__main__":
    main()
