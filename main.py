#!/usr/bin/env python3
"""The Funniest Toaster Error Message — make.fun entry.

Writes one line, at most 120 characters, to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR/entry.txt when the harness sets it): the error message
a kitchen toaster shows its owner when something goes wrong.

The line is a deadpan product-recall notice. The toaster is not broken; the
bread is. "It knows what it did" gives the bread a guilty past without
explaining it, so the joke lands on a single read and the appliance keeps
one calm, bureaucratic voice from the error code to the last word.
"""

import os
import sys

ENTRY_TEXT = "ERROR E12: The bread has been recalled. It knows what it did."

MAX_CHARS = 120


def output_dir():
    """Where the harness wants the artifact: env override, else /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def validate(text):
    """Mirror the sealed gate: UTF-8 text, 1 to 120 chars, not only
    whitespace, and a single line — fail loudly instead of shipping
    an entry the judge would never see."""
    if not isinstance(text, str):
        raise SystemExit("entry must be text")
    if not text.strip():
        raise SystemExit("entry is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be one line")
    if len(text) > MAX_CHARS:
        raise SystemExit(f"entry is {len(text)} chars, over the {MAX_CHARS} cap")
    text.encode("utf-8")


def main():
    validate(ENTRY_TEXT)
    out_path = os.path.join(output_dir(), "entry.txt")
    os.makedirs(output_dir(), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY_TEXT)
    with open(out_path, "rb") as f:
        written = f.read()
    if written != ENTRY_TEXT.encode("utf-8"):
        raise SystemExit("read-back mismatch: entry.txt does not match ENTRY_TEXT")
    print(f"wrote {out_path} ({len(ENTRY_TEXT)} chars, {len(written)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
