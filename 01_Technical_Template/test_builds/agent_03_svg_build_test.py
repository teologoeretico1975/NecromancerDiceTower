#!/usr/bin/env python3
"""Agent 03: SVG preflight checks for Necromancer Dice Tower technical sheets."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SVG_DIR = ROOT / "01_Technical_Template" / "svg"

FILES = [
    "sheet_01_body_a.svg",
    "sheet_02_body_b.svg",
    "sheet_03_ramps_ab.svg",
    "sheet_04_ramp_c.svg",
    "sheet_05_base_tray.svg",
]

COMMON_SUBSTRINGS = [
    ("width=210mm", 'width="210mm"'),
    ("height=297mm", 'height="297mm"'),
    ("viewBox", 'viewBox="0 0 210 297"'),
    ("legend", "LEGEND"),
    ("scale square text", "20 x 20 mm"),
    ("glue fill", 'fill="#e6e6e6"'),
]

RE_BLACK = re.compile(r"stroke\s*=\s*['\"]black['\"]", re.IGNORECASE)
RE_BLUE_DASH = re.compile(
    r"<[^>]*stroke\s*=\s*['\"]blue['\"][^>]*stroke-dasharray\s*=\s*['\"]4\s*,\s*2['\"][^>]*>"
    r"|<[^>]*stroke-dasharray\s*=\s*['\"]4\s*,\s*2['\"][^>]*stroke\s*=\s*['\"]blue['\"][^>]*>",
    re.IGNORECASE,
)
RE_RED_DOT = re.compile(
    r"<[^>]*stroke\s*=\s*['\"]red['\"][^>]*stroke-dasharray\s*=\s*['\"]1\s*,\s*2['\"][^>]*>"
    r"|<[^>]*stroke-dasharray\s*=\s*['\"]1\s*,\s*2['\"][^>]*stroke\s*=\s*['\"]red['\"][^>]*>",
    re.IGNORECASE,
)

ANCHOR_LABELS = ["A-L", "A-R", "B-L", "B-R", "C-L", "C-R"]
RAMP_LABELS = ["HIGH SIDE", "LOW SIDE", "FLOW -&gt;", "GLUE TO WALL"]


def check_file(path: Path) -> tuple[bool, list[str]]:
    if not path.exists():
        return False, ["missing file"]

    text = path.read_text(encoding="utf-8")
    missing: list[str] = []

    for label, token in COMMON_SUBSTRINGS:
        if token not in text:
            missing.append(label)

    if not RE_BLACK.search(text):
        missing.append("black cut line")
    if not RE_BLUE_DASH.search(text):
        missing.append("blue dashed valley")
    if not RE_RED_DOT.search(text):
        missing.append("red dotted mountain")

    if path.name in {"sheet_01_body_a.svg", "sheet_02_body_b.svg"}:
        for anchor in ANCHOR_LABELS:
            if anchor not in text:
                missing.append(f"anchor {anchor}")

    if path.name in {"sheet_03_ramps_ab.svg", "sheet_04_ramp_c.svg"}:
        for label in RAMP_LABELS:
            if label not in text:
                missing.append(f"label {label}")

    return len(missing) == 0, missing


def main() -> int:
    overall_ok = True
    print("Agent 03 SVG Build Test")
    print(f"SVG dir: {SVG_DIR}")

    for filename in FILES:
        file_path = SVG_DIR / filename
        ok, missing = check_file(file_path)
        status = "PASS" if ok else "FAIL"
        print(f"- {filename}: {status}")
        if missing:
            overall_ok = False
            for item in missing:
                print(f"  - missing: {item}")

    print(f"OVERALL: {'PASS' if overall_ok else 'FAIL'}")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
