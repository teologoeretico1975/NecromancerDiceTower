#!/usr/bin/env python3
"""Generate A4 technical SVG sheets for the Necromancer Dice Tower."""

from __future__ import annotations

import os
import re
from pathlib import Path

import svgwrite
from dotenv import load_dotenv

A4_WIDTH_MM = 210
A4_HEIGHT_MM = 297
STROKE_WIDTH = 0.5

CUT_STYLE = {"stroke": "black", "stroke_width": STROKE_WIDTH, "fill": "none"}
VALLEY_STYLE = {
    "stroke": "blue",
    "stroke_width": STROKE_WIDTH,
    "fill": "none",
    "stroke_dasharray": "4,2",
}
MOUNTAIN_STYLE = {
    "stroke": "red",
    "stroke_width": STROKE_WIDTH,
    "fill": "none",
    "stroke_dasharray": "1,2",
}

GLUE_TAB_FILL = "#e6e6e6"
TEXT_STYLE = {"font_size": "3.6px", "font_family": "Arial", "fill": "black"}

ROOT_DIR = Path(__file__).resolve().parent
SPECS_DIR = ROOT_DIR / "01_Technical_Template" / "specs"
SVG_DIR = ROOT_DIR / "01_Technical_Template" / "svg"


class SpecConfig:
    """Merged technical config from all markdown specs in specs/ directory."""

    def __init__(self) -> None:
        # v001 defaults
        self.front_w = 65.0
        self.side_w = 65.0
        self.back_w = 65.0
        self.panel_h = 190.0
        self.glue_tab_a = 10.0
        self.glue_tab_b = 10.0

        # ramp geometry
        self.ramp_width = 58.0
        self.ramp_length = 70.0
        self.side_tab = 10.0
        self.back_tab = 10.0
        self.modules = 8
        self.tread = 8.0
        self.rise = 3.0
        self.side_wall_h = 5.0
        self.use_v002_ramp_rules = False

        # tray
        self.tray_floor_w = 95.0
        self.tray_floor_h = 90.0
        self.tray_wall_h = 25.0
        self.tray_flap_w = 65.0
        self.tray_flap_h = 20.0


def parse_number_mm(text: str, pattern: str) -> float | None:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return None
    return float(match.group(1))


def parse_int(text: str, pattern: str) -> int | None:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return None
    return int(match.group(1))


def parse_range_midpoint_mm(text: str, pattern: str) -> float | None:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return None
    lo = float(match.group(1))
    hi = float(match.group(2))
    return (lo + hi) / 2.0


def specs_in_version_order() -> list[Path]:
    spec_files = sorted(SPECS_DIR.glob("technical_spec_v*.md"))
    if not spec_files:
        raise FileNotFoundError(f"No technical specs found in: {SPECS_DIR}")

    def version_key(path: Path) -> tuple[int, str]:
        m = re.search(r"v(\d+)", path.stem, flags=re.IGNORECASE)
        return (int(m.group(1)) if m else 0, path.stem)

    return sorted(spec_files, key=version_key)


def build_config_from_specs(spec_paths: list[Path]) -> SpecConfig:
    cfg = SpecConfig()

    for spec_path in spec_paths:
        text = spec_path.read_text(encoding="utf-8").strip()
        if not text:
            raise RuntimeError(f"Technical spec file is empty: {spec_path}")

        # Body dimensions
        val = parse_number_mm(text, r"\|\s*Front panel\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*[x×]\s*([0-9]+(?:\.[0-9]+)?)\s*mm")
        if val is not None:
            # Width is first match group in this specific table row pattern.
            row = re.search(
                r"\|\s*Front panel\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*[x×]\s*([0-9]+(?:\.[0-9]+)?)\s*mm",
                text,
                flags=re.IGNORECASE,
            )
            if row:
                cfg.front_w = float(row.group(1))
                cfg.panel_h = float(row.group(2))

        row_side = re.search(
            r"\|\s*Left side panel\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*[x×]\s*([0-9]+(?:\.[0-9]+)?)\s*mm",
            text,
            flags=re.IGNORECASE,
        )
        if row_side:
            cfg.side_w = float(row_side.group(1))

        row_back = re.search(
            r"\|\s*Back panel\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*[x×]\s*([0-9]+(?:\.[0-9]+)?)\s*mm",
            text,
            flags=re.IGNORECASE,
        )
        if row_back:
            cfg.back_w = float(row_back.group(1))

        row_tab = re.search(
            r"\|\s*Glue tab\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*[x×]\s*([0-9]+(?:\.[0-9]+)?)\s*mm",
            text,
            flags=re.IGNORECASE,
        )
        if row_tab:
            cfg.glue_tab_a = float(row_tab.group(1))

        row_tab_a = re.search(
            r"\|\s*Glue tab A\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*[x×]\s*([0-9]+(?:\.[0-9]+)?)\s*mm",
            text,
            flags=re.IGNORECASE,
        )
        if row_tab_a:
            cfg.glue_tab_a = float(row_tab_a.group(1))

        row_tab_b = re.search(
            r"\|\s*Glue tab B\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*[x×]\s*([0-9]+(?:\.[0-9]+)?)\s*mm",
            text,
            flags=re.IGNORECASE,
        )
        if row_tab_b:
            cfg.glue_tab_b = float(row_tab_b.group(1))

        # Ramp values: use newer specs to override older values.
        ramp_w = parse_number_mm(text, r"Ramp width\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*mm")
        if ramp_w is not None:
            cfg.ramp_width = ramp_w

        ramp_w_range = parse_range_midpoint_mm(text, r"Ramp clear width\s*\|\s*([0-9]+(?:\.[0-9]+)?)-([0-9]+(?:\.[0-9]+)?)\s*mm")
        if ramp_w_range is not None:
            cfg.ramp_width = ramp_w_range

        ramp_len = parse_number_mm(text, r"Ramp length\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*mm")
        if ramp_len is not None:
            cfg.ramp_length = ramp_len

        run_len = parse_range_midpoint_mm(text, r"Ramp effective run length\s*\|\s*([0-9]+(?:\.[0-9]+)?)-([0-9]+(?:\.[0-9]+)?)\s*mm")
        if run_len is not None:
            cfg.ramp_length = run_len

        side_tab = parse_number_mm(text, r"Side tabs\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*mm")
        if side_tab is not None:
            cfg.side_tab = side_tab

        back_tab = parse_number_mm(text, r"Back tab\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*mm")
        if back_tab is not None:
            cfg.back_tab = back_tab

        tread = parse_number_mm(text, r"Tread p\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*mm")
        if tread is not None:
            cfg.tread = tread

        rise = parse_number_mm(text, r"Rise h\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*mm")
        if rise is not None:
            cfg.rise = rise

        modules = parse_int(text, r"Number of modules per ramp\s*\|\s*([0-9]+)")
        if modules is not None:
            cfg.modules = modules

        wall_h = parse_number_mm(text, r"Side wall height on ramp\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*mm")
        if wall_h is not None:
            cfg.side_wall_h = wall_h

        if "Technical Specification v002" in text or "Stepped Profile" in text:
            cfg.use_v002_ramp_rules = True

        # Base tray
        tray_row = re.search(
            r"\|\s*Tray floor\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*[x×]\s*([0-9]+(?:\.[0-9]+)?)\s*mm",
            text,
            flags=re.IGNORECASE,
        )
        if tray_row:
            cfg.tray_floor_w = float(tray_row.group(1))
            cfg.tray_floor_h = float(tray_row.group(2))

        fw = parse_number_mm(text, r"\|\s*Front wall\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*[x×]\s*([0-9]+(?:\.[0-9]+)?)\s*mm")
        if fw is not None:
            row = re.search(
                r"\|\s*Front wall\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*[x×]\s*([0-9]+(?:\.[0-9]+)?)\s*mm",
                text,
                flags=re.IGNORECASE,
            )
            if row:
                cfg.tray_wall_h = float(row.group(2))

        flap = re.search(
            r"\|\s*Back connection flap\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*[x×]\s*([0-9]+(?:\.[0-9]+)?)\s*mm",
            text,
            flags=re.IGNORECASE,
        )
        if flap:
            cfg.tray_flap_w = float(flap.group(1))
            cfg.tray_flap_h = float(flap.group(2))

    return cfg


def mm(value: float) -> str:
    return f"{value}mm"


def create_drawing(output_path: Path, title: str) -> svgwrite.Drawing:
    dwg = svgwrite.Drawing(
        filename=str(output_path),
        size=(mm(A4_WIDTH_MM), mm(A4_HEIGHT_MM)),
        viewBox=f"0 0 {A4_WIDTH_MM} {A4_HEIGHT_MM}",
        profile="full",
    )
    dwg.set_desc(f"{title} | A4 portrait 210x297 mm | target export 96 dpi")
    dwg.add(dwg.text(title, insert=(10, 10), **TEXT_STYLE))
    return dwg


def add_rect(dwg: svgwrite.Drawing, x: float, y: float, w: float, h: float, style: dict) -> None:
    dwg.add(dwg.rect(insert=(x, y), size=(w, h), **style))


def add_scale_square(dwg: svgwrite.Drawing) -> None:
    x = A4_WIDTH_MM - 10 - 20
    y = A4_HEIGHT_MM - 10 - 20
    add_rect(dwg, x, y, 20, 20, CUT_STYLE)
    dwg.add(dwg.text("20 x 20 mm", insert=(x - 18, y + 24), **TEXT_STYLE))


def add_legend(dwg: svgwrite.Drawing) -> None:
    lx, ly = 10, A4_HEIGHT_MM - 32
    dwg.add(dwg.text("LEGEND", insert=(lx, ly), **TEXT_STYLE))
    dwg.add(dwg.line(start=(lx, ly + 4), end=(lx + 18, ly + 4), **CUT_STYLE))
    dwg.add(dwg.text("CUT", insert=(lx + 21, ly + 5), **TEXT_STYLE))
    dwg.add(dwg.line(start=(lx, ly + 10), end=(lx + 18, ly + 10), **VALLEY_STYLE))
    dwg.add(dwg.text("VALLEY FOLD", insert=(lx + 21, ly + 11), **TEXT_STYLE))
    dwg.add(dwg.line(start=(lx, ly + 16), end=(lx + 18, ly + 16), **MOUNTAIN_STYLE))
    dwg.add(dwg.text("MOUNTAIN FOLD", insert=(lx + 21, ly + 17), **TEXT_STYLE))
    dwg.add(dwg.rect(insert=(lx, ly + 20), size=(18, 6), fill=GLUE_TAB_FILL, stroke="none"))
    dwg.add(dwg.text("GLUE TAB", insert=(lx + 21, ly + 25), **TEXT_STYLE))


def add_common(dwg: svgwrite.Drawing) -> None:
    add_legend(dwg)
    add_scale_square(dwg)


def draw_anchor_tick(dwg: svgwrite.Drawing, x: float, y: float, label: str) -> None:
    dwg.add(dwg.line(start=(x - 4, y), end=(x + 4, y), **VALLEY_STYLE))
    dwg.add(dwg.text(label, insert=(x + 5, y + 1.5), **TEXT_STYLE))


def draw_sheet_01_body_a(cfg: SpecConfig) -> Path:
    output = SVG_DIR / "sheet_01_body_a.svg"
    dwg = create_drawing(output, "Sheet 01 - Body Part A")
    x0, y0, h = 20, 30, cfg.panel_h
    tab_w, front_w, left_w = cfg.glue_tab_a, cfg.front_w, cfg.side_w
    dwg.add(dwg.rect(insert=(x0, y0), size=(tab_w, h), fill=GLUE_TAB_FILL, stroke="none"))
    add_rect(dwg, x0, y0, tab_w + front_w + left_w, h, CUT_STYLE)
    dwg.add(dwg.line(start=(x0 + tab_w, y0), end=(x0 + tab_w, y0 + h), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0 + tab_w + front_w, y0), end=(x0 + tab_w + front_w, y0 + h), **VALLEY_STYLE))
    dwg.add(dwg.text("GLUE TAB", insert=(x0 + 1.0, y0 + 95), **TEXT_STYLE))
    dwg.add(dwg.text("FRONT", insert=(x0 + tab_w + 23, y0 + 95), **TEXT_STYLE))
    dwg.add(dwg.text("LEFT SIDE", insert=(x0 + tab_w + front_w + 18, y0 + 95), **TEXT_STYLE))

    if cfg.use_v002_ramp_rules:
        # v002 requires short anchor ticks instead of long full guide lines.
        panel_left_x = x0 + tab_w
        panel_right_x = x0 + tab_w + front_w + left_w
        bottom_y = y0 + h
        anchor_map = [
            ("A-L", 150.0),
            ("A-R", 140.0),
            ("B-L", 90.0),
            ("B-R", 100.0),
            ("C-L", 50.0),
            ("C-R", 40.0),
        ]
        for label, y_from_bottom in anchor_map:
            y = bottom_y - y_from_bottom
            x = panel_left_x if label.endswith("-L") else panel_right_x
            draw_anchor_tick(dwg, x, y, f"{label} {int(y_from_bottom)}mm")

    add_common(dwg)
    dwg.save()
    return output


def draw_sheet_02_body_b(cfg: SpecConfig) -> Path:
    output = SVG_DIR / "sheet_02_body_b.svg"
    dwg = create_drawing(output, "Sheet 02 - Body Part B")
    x0, y0, h = 20, 30, cfg.panel_h
    tab_a_w, back_w, right_w, tab_b_w = cfg.glue_tab_a, cfg.back_w, cfg.side_w, cfg.glue_tab_b
    total_w = tab_a_w + back_w + right_w + tab_b_w
    dwg.add(dwg.rect(insert=(x0, y0), size=(tab_a_w, h), fill=GLUE_TAB_FILL, stroke="none"))
    dwg.add(dwg.rect(insert=(x0 + tab_a_w + back_w + right_w, y0), size=(tab_b_w, h), fill=GLUE_TAB_FILL, stroke="none"))
    add_rect(dwg, x0, y0, total_w, h, CUT_STYLE)
    dwg.add(dwg.line(start=(x0 + tab_a_w, y0), end=(x0 + tab_a_w, y0 + h), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0 + tab_a_w + back_w, y0), end=(x0 + tab_a_w + back_w, y0 + h), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0 + tab_a_w + back_w + right_w, y0), end=(x0 + tab_a_w + back_w + right_w, y0 + h), **VALLEY_STYLE))
    dwg.add(dwg.text("GLUE TAB A", insert=(x0 + 0.8, y0 + 95), **TEXT_STYLE))
    dwg.add(dwg.text("BACK", insert=(x0 + tab_a_w + 25, y0 + 95), **TEXT_STYLE))
    dwg.add(dwg.text("RIGHT SIDE", insert=(x0 + tab_a_w + back_w + 14, y0 + 95), **TEXT_STYLE))
    dwg.add(dwg.text("GLUE TAB B", insert=(x0 + tab_a_w + back_w + right_w + 0.8, y0 + 95), **TEXT_STYLE))

    if cfg.use_v002_ramp_rules:
        panel_left_x = x0 + tab_a_w
        panel_right_x = x0 + tab_a_w + back_w + right_w
        bottom_y = y0 + h
        anchor_map = [
            ("A-L", 150.0),
            ("A-R", 140.0),
            ("B-L", 90.0),
            ("B-R", 100.0),
            ("C-L", 50.0),
            ("C-R", 40.0),
        ]
        for label, y_from_bottom in anchor_map:
            y = bottom_y - y_from_bottom
            x = panel_left_x if label.endswith("-L") else panel_right_x
            draw_anchor_tick(dwg, x, y, f"{label} {int(y_from_bottom)}mm")

    add_common(dwg)
    dwg.save()
    return output


def draw_ramp(dwg: svgwrite.Drawing, cfg: SpecConfig, x0: float, y0: float, label: str) -> None:
    body_w, body_l = cfg.ramp_width, cfg.ramp_length
    tab_side, tab_back = cfg.side_tab, cfg.back_tab
    total_w = tab_side + body_w + tab_side
    dwg.add(dwg.rect(insert=(x0, y0), size=(tab_side, body_l), fill=GLUE_TAB_FILL, stroke="none"))
    dwg.add(dwg.rect(insert=(x0 + tab_side + body_w, y0), size=(tab_side, body_l), fill=GLUE_TAB_FILL, stroke="none"))
    dwg.add(dwg.rect(insert=(x0 + tab_side, y0 - tab_back), size=(body_w, tab_back), fill=GLUE_TAB_FILL, stroke="none"))
    add_rect(dwg, x0, y0, total_w, body_l, CUT_STYLE)
    add_rect(dwg, x0 + tab_side, y0 - tab_back, body_w, tab_back, CUT_STYLE)
    dwg.add(dwg.line(start=(x0 + tab_side, y0), end=(x0 + tab_side, y0 + body_l), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0 + tab_side + body_w, y0), end=(x0 + tab_side + body_w, y0 + body_l), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0 + tab_side, y0), end=(x0 + tab_side + body_w, y0), **MOUNTAIN_STYLE))

    if cfg.use_v002_ramp_rules:
        # Draw stepped fold map lines from v002 parameters.
        usable_run = min(body_l, cfg.modules * cfg.tread)
        for i in range(1, cfg.modules):
            step_y = y0 + min(i * cfg.tread, usable_run)
            style = VALLEY_STYLE if i % 2 else MOUNTAIN_STYLE
            dwg.add(dwg.line(start=(x0 + tab_side, step_y), end=(x0 + tab_side + body_w, step_y), **style))

        # Side wall fold lines for required 4-6 mm walls.
        wall_h = cfg.side_wall_h
        dwg.add(dwg.line(start=(x0 + tab_side + wall_h, y0), end=(x0 + tab_side + wall_h, y0 + body_l), **VALLEY_STYLE))
        dwg.add(
            dwg.line(
                start=(x0 + tab_side + body_w - wall_h, y0),
                end=(x0 + tab_side + body_w - wall_h, y0 + body_l),
                **VALLEY_STYLE,
            )
        )

        dwg.add(dwg.text(f"{label}", insert=(x0 + tab_side + 2, y0 + 12), **TEXT_STYLE))
        dwg.add(dwg.text("HIGH SIDE", insert=(x0 + tab_side + 2, y0 + 20), **TEXT_STYLE))
        dwg.add(dwg.text("LOW SIDE", insert=(x0 + tab_side + body_w - 18, y0 + 20), **TEXT_STYLE))
        dwg.add(dwg.text("GLUE TO WALL", insert=(x0 + 0.8, y0 + 35), **TEXT_STYLE))
        dwg.add(dwg.text("GLUE TO WALL", insert=(x0 + tab_side + body_w + 0.8, y0 + 35), **TEXT_STYLE))
        dwg.add(dwg.text("BACK TAB", insert=(x0 + tab_side + body_w / 2 - 8, y0 - 2), **TEXT_STYLE))
        dwg.add(dwg.text("FLOW ->", insert=(x0 + tab_side + 2, y0 + body_l - 4), **TEXT_STYLE))
    else:
        dwg.add(dwg.text(label, insert=(x0 + tab_side + 20, y0 + 36), **TEXT_STYLE))


def draw_sheet_03_ramps_ab(cfg: SpecConfig) -> Path:
    output = SVG_DIR / "sheet_03_ramps_ab.svg"
    dwg = create_drawing(output, "Sheet 03 - Ramps A and B")
    draw_ramp(dwg, cfg, x0=20, y0=70, label="RAMP A")
    draw_ramp(dwg, cfg, x0=110, y0=70, label="RAMP B")
    add_common(dwg)
    dwg.save()
    return output


def draw_sheet_04_ramp_c(cfg: SpecConfig) -> Path:
    output = SVG_DIR / "sheet_04_ramp_c.svg"
    dwg = create_drawing(output, "Sheet 04 - Ramp C")
    draw_ramp(dwg, cfg, x0=66, y0=90, label="RAMP C")
    add_common(dwg)
    dwg.save()
    return output


def draw_sheet_05_base_tray(cfg: SpecConfig) -> Path:
    output = SVG_DIR / "sheet_05_base_tray.svg"
    dwg = create_drawing(output, "Sheet 05 - Base Tray")
    x0, y0 = 45, 95
    floor_w, floor_h = cfg.tray_floor_w, cfg.tray_floor_h
    wall_h = cfg.tray_wall_h
    flap_w, flap_h = cfg.tray_flap_w, cfg.tray_flap_h
    add_rect(dwg, x0, y0, floor_w, floor_h, CUT_STYLE)
    dwg.add(dwg.rect(insert=(x0, y0 - wall_h), size=(floor_w, wall_h), fill=GLUE_TAB_FILL, stroke="none"))
    dwg.add(dwg.rect(insert=(x0, y0 + floor_h), size=(floor_w, wall_h), fill=GLUE_TAB_FILL, stroke="none"))
    dwg.add(dwg.rect(insert=(x0 - wall_h, y0), size=(wall_h, floor_h), fill=GLUE_TAB_FILL, stroke="none"))
    dwg.add(dwg.rect(insert=(x0 + floor_w, y0), size=(wall_h, floor_h), fill=GLUE_TAB_FILL, stroke="none"))
    dwg.add(dwg.rect(insert=(x0 + (floor_w - flap_w) / 2, y0 + floor_h + wall_h), size=(flap_w, flap_h), fill=GLUE_TAB_FILL, stroke="none"))
    add_rect(dwg, x0, y0 - wall_h, floor_w, wall_h, CUT_STYLE)
    add_rect(dwg, x0, y0 + floor_h, floor_w, wall_h, CUT_STYLE)
    add_rect(dwg, x0 - wall_h, y0, wall_h, floor_h, CUT_STYLE)
    add_rect(dwg, x0 + floor_w, y0, wall_h, floor_h, CUT_STYLE)
    add_rect(dwg, x0 + (floor_w - flap_w) / 2, y0 + floor_h + wall_h, flap_w, flap_h, CUT_STYLE)
    dwg.add(dwg.line(start=(x0, y0), end=(x0 + floor_w, y0), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0, y0 + floor_h), end=(x0 + floor_w, y0 + floor_h), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0, y0), end=(x0, y0 + floor_h), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0 + floor_w, y0), end=(x0 + floor_w, y0 + floor_h), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0 + (floor_w - flap_w) / 2, y0 + floor_h + wall_h), end=(x0 + (floor_w - flap_w) / 2 + flap_w, y0 + floor_h + wall_h), **MOUNTAIN_STYLE))
    add_common(dwg)
    dwg.save()
    return output


def main() -> None:
    load_dotenv(ROOT_DIR / ".env")
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Missing ANTHROPIC_API_KEY in .env")

    spec_paths = specs_in_version_order()
    cfg = build_config_from_specs(spec_paths)
    SVG_DIR.mkdir(parents=True, exist_ok=True)

    generated_by = ", ".join(path.name for path in spec_paths)
    print(f"Loaded specs: {generated_by}")

    for gen in [
        lambda: draw_sheet_01_body_a(cfg),
        lambda: draw_sheet_02_body_b(cfg),
        lambda: draw_sheet_03_ramps_ab(cfg),
        lambda: draw_sheet_04_ramp_c(cfg),
        lambda: draw_sheet_05_base_tray(cfg),
    ]:
        path = gen()
        print(f"Generated: {path}")


if __name__ == "__main__":
    main()
