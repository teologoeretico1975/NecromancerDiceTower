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


def get_svg_output_path(cfg: SpecConfig, base_name: str) -> Path:
    """Construct SVG output path with mode suffix (e.g., _beginner)."""
    if cfg.output_mode == "beginner":
        name_without_ext = base_name.replace(".svg", "")
        return SVG_DIR / f"{name_without_ext}_beginner.svg"
    return SVG_DIR / base_name


class SpecConfig:
    """Merged technical config from all markdown specs in specs/ directory."""

    def __init__(self) -> None:
        # Output mode: "standard" (compact), "beginner" (extra guidance)
        self.output_mode = "standard"

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
        self.tray_floor_w = 100.0
        self.tray_floor_h = 130.0
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
            r"\|\s*(?:Catch\s+)?Tray floor\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*[x×]\s*([0-9]+(?:\.[0-9]+)?)\s*mm",
            text,
            flags=re.IGNORECASE,
        )
        if tray_row:
            cfg.tray_floor_w = float(tray_row.group(1))
            cfg.tray_floor_h = float(tray_row.group(2))

        tray_wall_row = re.search(
            r"\|\s*Catch tray side wall \(long\)\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*[x×]\s*([0-9]+(?:\.[0-9]+)?)\s*mm",
            text,
            flags=re.IGNORECASE,
        )
        if tray_wall_row:
            cfg.tray_wall_h = float(tray_wall_row.group(2))

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


def add_rotated_tab_label(
    dwg: svgwrite.Drawing,
    label: str,
    cx: float,
    cy: float,
    angle: float,
) -> None:
    dwg.add(
        dwg.text(
            label,
            insert=(cx, cy),
            transform=f"rotate({angle} {cx} {cy})",
            text_anchor="middle",
            dominant_baseline="middle",
            **TEXT_STYLE,
        )
    )


def draw_ramp_3d_example(dwg: svgwrite.Drawing, x: float, y: float) -> None:
    """Small wireframe 3D-style fold example for human assembly guidance."""
    dwg.add(dwg.text("3D EXAMPLE (folded profile)", insert=(x, y - 4), **TEXT_STYLE))

    # Top and bottom rails (isometric-like projection)
    top = [(x + 0, y + 3), (x + 8, y + 0), (x + 24, y + 0), (x + 32, y + 3)]
    bottom = [(x + 0, y + 15), (x + 8, y + 12), (x + 24, y + 12), (x + 32, y + 15)]
    dwg.add(dwg.polyline(points=top, **CUT_STYLE))
    dwg.add(dwg.polyline(points=bottom, **CUT_STYLE))

    # Side edges
    dwg.add(dwg.line(start=top[0], end=bottom[0], **CUT_STYLE))
    dwg.add(dwg.line(start=top[1], end=bottom[1], **CUT_STYLE))
    dwg.add(dwg.line(start=top[2], end=bottom[2], **CUT_STYLE))
    dwg.add(dwg.line(start=top[3], end=bottom[3], **CUT_STYLE))

    # Internal zig-zag crease profile (alternating mountain/valley)
    p1 = (x + 8, y + 6)
    p2 = (x + 12, y + 9)
    p3 = (x + 16, y + 6)
    p4 = (x + 20, y + 9)
    p5 = (x + 24, y + 6)
    dwg.add(dwg.line(start=p1, end=p2, **MOUNTAIN_STYLE))
    dwg.add(dwg.line(start=p2, end=p3, **VALLEY_STYLE))
    dwg.add(dwg.line(start=p3, end=p4, **MOUNTAIN_STYLE))
    dwg.add(dwg.line(start=p4, end=p5, **VALLEY_STYLE))

    dwg.add(dwg.text("M/V", insert=(x + 33, y + 10), **TEXT_STYLE))


def draw_ramp_fold_sequence(dwg: svgwrite.Drawing, x: float, y: float) -> None:
    """Draw 1-2-3 visual sequence LARGE and CLEAR: flat, first fold, glued. For Beginner mode.
    
    This is the PRIMARY guide, not cramped in a corner. Sized to be readable by kids.
    """
    # Title
    dwg.add(dwg.text("HOW TO FOLD YOUR RAMP — 3 SIMPLE STEPS", insert=(x, y), 
                     font_size="5px", font_family="Arial", font_weight="bold", fill="black"))
    
    # ===== STAGE 1: FLAT =====
    y1 = y + 12
    dwg.add(dwg.text("1. FLAT NET", insert=(x, y1 - 2), 
                     font_size="5px", font_family="Arial", font_weight="bold", fill="black"))
    
    # Large flat rectangle with label
    dwg.add(dwg.rect(insert=(x + 2, y1), size=(20, 14), fill="white", stroke="black", stroke_width=1))
    dwg.add(dwg.text("all pieces", insert=(x + 8, y1 + 8), 
                     font_size="3.5px", font_family="Arial", fill="black"))
    dwg.add(dwg.text("flat & unfolded", insert=(x + 5, y1 + 12), 
                     font_size="3.5px", font_family="Arial", fill="black"))
    
    # Arrow pointing right
    dwg.add(dwg.line(start=(x + 25, y1 + 7), end=(x + 32, y1 + 7), stroke="black", stroke_width=1))
    dwg.add(dwg.polygon(points=[(x + 32, y1 + 7), (x + 29, y1 + 5), (x + 29, y1 + 9)], fill="black"))
    
    # ===== STAGE 2: SCORE & FOLD =====
    y2 = y + 12
    dwg.add(dwg.text("2. SCORE & FOLD", insert=(x + 38, y2 - 2), 
                     font_size="5px", font_family="Arial", font_weight="bold", fill="black"))
    
    # Show bottom edge starting to fold up (simplified)
    dwg.add(dwg.rect(insert=(x + 38, y2), size=(20, 7), fill="white", stroke="black", stroke_width=1))
    # Add fold lines hint
    dwg.add(dwg.line(start=(x + 38, y2 + 4), end=(x + 58, y2 + 4), 
                     stroke="blue", stroke_width=1, stroke_dasharray="3,2"))
    dwg.add(dwg.text("fold here", insert=(x + 41, y2 + 11), 
                     font_size="3.5px", font_family="Arial", fill="blue"))
    
    # Another section folding up
    dwg.add(dwg.polyline(points=[(x + 38, y2 + 7), (x + 48, y2 + 13)], 
                         stroke="blue", stroke_width=1, stroke_dasharray="3,2", fill="none"))
    dwg.add(dwg.polyline(points=[(x + 58, y2 + 7), (x + 48, y2 + 13)], 
                         stroke="blue", stroke_width=1, stroke_dasharray="3,2", fill="none"))
    
    # Arrow
    dwg.add(dwg.line(start=(x + 61, y2 + 7), end=(x + 68, y2 + 7), stroke="black", stroke_width=1))
    dwg.add(dwg.polygon(points=[(x + 68, y2 + 7), (x + 65, y2 + 5), (x + 65, y2 + 9)], fill="black"))
    
    # ===== STAGE 3: GLUE & ASSEMBLE =====
    y3 = y + 12
    dwg.add(dwg.text("3. GLUE & DONE", insert=(x + 75, y3 - 2), 
                     font_size="5px", font_family="Arial", font_weight="bold", fill="black"))
    
    # Final assembled shape (compact accordion)
    dwg.add(dwg.polyline(points=[(x + 75, y3 + 3), (x + 82, y3), (x + 89, y3 + 3), (x + 96, y3)], 
                         stroke="black", stroke_width=1.5, fill="none"))
    dwg.add(dwg.polyline(points=[(x + 75, y3 + 14), (x + 82, y3 + 17), (x + 89, y3 + 14), (x + 96, y3 + 17)], 
                         stroke="black", stroke_width=1.5, fill="none"))
    
    # Glue tabs on sides (little gray boxes)
    dwg.add(dwg.rect(insert=(x + 73, y3 + 5), size=(3, 4), fill="#cccccc", stroke="blue", stroke_width=0.5))
    dwg.add(dwg.rect(insert=(x + 97, y3 + 5), size=(3, 4), fill="#cccccc", stroke="blue", stroke_width=0.5))
    
    dwg.add(dwg.text("glue", insert=(x + 80, y3 + 20), 
                     font_size="3.5px", font_family="Arial", fill="blue"))
    dwg.add(dwg.text("tabs", insert=(x + 80, y3 + 24), 
                     font_size="3.5px", font_family="Arial", fill="blue"))
    
    # Add summary text below
    y_summary = y + 35
    dwg.add(dwg.text("TIP: Fold at BACK TAB (top) first, then work downward.", 
                     insert=(x, y_summary), 
                     font_size="4px", font_family="Arial", fill="black", font_weight="bold"))
    dwg.add(dwg.text("All BLUE dashed lines = VALLEY folds (crease inward ↓)", 
                     insert=(x, y_summary + 5), 
                     font_size="3.5px", font_family="Arial", fill="blue"))
    dwg.add(dwg.text("All RED dotted lines = MOUNTAIN folds (crease outward ↑)", 
                     insert=(x, y_summary + 10), 
                     font_size="3.5px", font_family="Arial", fill="red"))


def draw_fold_arrow(dwg: svgwrite.Drawing, x: float, y: float, label: str = "FOLD") -> None:
    dwg.add(dwg.line(start=(x + 3, y + 8), end=(x + 3, y), stroke="black", stroke_width=0.5))
    dwg.add(dwg.polygon(points=[(x + 3, y - 1.5), (x + 1.5, y + 1), (x + 4.5, y + 1)], fill="black"))
    dwg.add(dwg.text(label, insert=(x + 6, y + 1), **TEXT_STYLE))


def draw_fold_callout(dwg: svgwrite.Drawing, x: float, y: float, text: str, side: str = "right") -> None:
    if side == "left":
        dwg.add(dwg.line(start=(x, y), end=(x - 10, y), stroke="black", stroke_width=0.5))
        dwg.add(dwg.polygon(points=[(x, y), (x - 2.2, y - 1.3), (x - 2.2, y + 1.3)], fill="black"))
        dwg.add(dwg.text(text, insert=(x - 34, y + 1.2), **TEXT_STYLE))
    else:
        dwg.add(dwg.line(start=(x, y), end=(x + 10, y), stroke="black", stroke_width=0.5))
        dwg.add(dwg.polygon(points=[(x, y), (x + 2.2, y - 1.3), (x + 2.2, y + 1.3)], fill="black"))
        dwg.add(dwg.text(text, insert=(x + 12, y + 1.2), **TEXT_STYLE))


def draw_sheet_01_body_a(cfg: SpecConfig) -> Path:
    output = get_svg_output_path(cfg, "sheet_01_body_a.svg")
    dwg = create_drawing(output, "Sheet 01 - Body Part A")
    x0, y0, h = 20, 30, cfg.panel_h
    tab_w, front_w, left_w = cfg.glue_tab_a, cfg.front_w, cfg.side_w
    dwg.add(dwg.rect(insert=(x0, y0), size=(tab_w, h), fill=GLUE_TAB_FILL, stroke="none"))
    add_rect(dwg, x0, y0, tab_w + front_w + left_w, h, CUT_STYLE)
    dwg.add(dwg.line(start=(x0 + tab_w, y0), end=(x0 + tab_w, y0 + h), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0 + tab_w + front_w, y0), end=(x0 + tab_w + front_w, y0 + h), **VALLEY_STYLE))
    dwg.add(dwg.text("F1", insert=(x0 + tab_w + 1.2, y0 + 8), **TEXT_STYLE))
    dwg.add(dwg.text("F2", insert=(x0 + tab_w + front_w + 1.2, y0 + 8), **TEXT_STYLE))
    add_rotated_tab_label(dwg, "GLUE TAB", x0 + tab_w / 2, y0 + h / 2, -90)
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

    dwg.add(dwg.text("FOLD GUIDE: 1) SCORE BLUE DASHED lines (F1/F2).", insert=(10, 22), **TEXT_STYLE))
    dwg.add(dwg.text("2) FOLD F1/F2 inward to 90°.  3) BLACK SOLID lines = CUT ONLY.", insert=(10, 26), **TEXT_STYLE))
    dwg.add(dwg.text("NOTE: If BLUE touches BLACK edge, treat it as FOLD line.", insert=(10, 258), **TEXT_STYLE))

    add_common(dwg)
    dwg.save()
    return output


def draw_sheet_02_body_b(cfg: SpecConfig) -> Path:
    output = get_svg_output_path(cfg, "sheet_02_body_b.svg")
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
    dwg.add(dwg.text("F1", insert=(x0 + tab_a_w + 1.2, y0 + 8), **TEXT_STYLE))
    dwg.add(dwg.text("F2", insert=(x0 + tab_a_w + back_w + 1.2, y0 + 8), **TEXT_STYLE))
    dwg.add(dwg.text("F3", insert=(x0 + tab_a_w + back_w + right_w + 1.2, y0 + 8), **TEXT_STYLE))
    add_rotated_tab_label(dwg, "GLUE TAB A", x0 + tab_a_w / 2, y0 + h / 2, -90)
    dwg.add(dwg.text("BACK", insert=(x0 + tab_a_w + 25, y0 + 95), **TEXT_STYLE))
    dwg.add(dwg.text("RIGHT SIDE", insert=(x0 + tab_a_w + back_w + 14, y0 + 95), **TEXT_STYLE))
    add_rotated_tab_label(
        dwg,
        "GLUE TAB B",
        x0 + tab_a_w + back_w + right_w + tab_b_w / 2,
        y0 + h / 2,
        90,
    )

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

    dwg.add(dwg.text("FOLD GUIDE: 1) SCORE BLUE DASHED lines (F1/F2/F3).", insert=(10, 22), **TEXT_STYLE))
    dwg.add(dwg.text("2) FOLD F1/F2/F3 inward to 90°.  3) BLACK SOLID lines = CUT ONLY.", insert=(10, 26), **TEXT_STYLE))
    dwg.add(dwg.text("NOTE: If BLUE touches BLACK edge, treat it as FOLD line.", insert=(10, 258), **TEXT_STYLE))

    add_common(dwg)
    dwg.save()
    return output


def draw_ramp(
    dwg: svgwrite.Drawing,
    cfg: SpecConfig,
    x0: float,
    y0: float,
    label: str,
    flow_direction: str = "L->R",
) -> None:
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

        flow_is_left_to_right = flow_direction.upper() == "L->R"
        high_x = x0 + tab_side + 2 if flow_is_left_to_right else x0 + tab_side + body_w - 18
        low_x = x0 + tab_side + body_w - 18 if flow_is_left_to_right else x0 + tab_side + 2
        flow_text = "FLOW ->" if flow_is_left_to_right else "FLOW <-"

        dwg.add(dwg.text(f"{label}", insert=(x0 + tab_side + 2, y0 + 12), **TEXT_STYLE))
        dwg.add(dwg.text("HIGH SIDE", insert=(high_x, y0 + 20), **TEXT_STYLE))
        dwg.add(dwg.text("LOW SIDE", insert=(low_x, y0 + 20), **TEXT_STYLE))
        add_rotated_tab_label(dwg, "GLUE TO WALL", x0 + tab_side / 2, y0 + body_l / 2, -90)
        add_rotated_tab_label(
            dwg,
            "GLUE TO WALL",
            x0 + tab_side + body_w + tab_side / 2,
            y0 + body_l / 2,
            90,
        )
        dwg.add(dwg.text("BACK TAB", insert=(x0 + tab_side + body_w / 2 - 8, y0 - 2), **TEXT_STYLE))
        dwg.add(dwg.text(flow_text, insert=(x0 + tab_side + 2, y0 + body_l - 4), **TEXT_STYLE))

        # Human-readable geometry hints for the "double fold" interpretation.
        # Only show extra text in STANDARD mode (Beginner mode has visual guide on a separate section)
        if cfg.output_mode == "standard":
            dwg.add(dwg.text("OUTER BLUE vertical = TAB fold", insert=(x0 + tab_side + 1, y0 + body_l + 7), **TEXT_STYLE))
            dwg.add(
                dwg.text(
                    f"INNER BLUE vertical = SIDE-WALL fold ({int(cfg.side_wall_h)}mm)",
                    insert=(x0 + tab_side + 1, y0 + body_l + 12),
                    **TEXT_STYLE,
                )
            )
    else:
        dwg.add(dwg.text(label, insert=(x0 + tab_side + 20, y0 + 36), **TEXT_STYLE))


def draw_sheet_03_ramps_ab(cfg: SpecConfig) -> Path:
    output = get_svg_output_path(cfg, "sheet_03_ramps_ab.svg")
    dwg = create_drawing(output, "Sheet 03 - Ramps A and B")
    dwg.add(dwg.text("GEOMETRIC DEVELOPMENT (v002): accordion/stepped profile.", insert=(10, 16), **TEXT_STYLE))
    dwg.add(
        dwg.text(
            f"Pitch p={int(cfg.tread)}mm, rise h={cfg.rise:.1f}mm, modules={cfg.modules}.",
            insert=(10, 22),
            **TEXT_STYLE,
        )
    )
    dwg.add(dwg.text("Horizontal folds alternate M/V from BACK TAB hinge (red then blue...).", insert=(10, 28), **TEXT_STYLE))
    dwg.add(dwg.text("Flow directions: RAMP A L->R, RAMP B R->L.", insert=(10, 34), **TEXT_STYLE))
    draw_ramp_3d_example(dwg, x=148, y=13)
    
    if cfg.output_mode == "beginner":
        # Draw large 1-2-3 fold sequence at top for visibility
        draw_ramp_fold_sequence(dwg, x=5, y=45)
        # Draw only RAMP A in beginner mode, positioned lower, at full size for clarity
        dwg.add(dwg.text("RAMP A (follow 1-2-3 steps above):", insert=(10, 110), **TEXT_STYLE))
        draw_ramp(dwg, cfg, x0=20, y0=130, label="RAMP A", flow_direction="L->R")
    else:
        # Standard mode: both ramps side by side
        draw_ramp(dwg, cfg, x0=20, y0=70, label="RAMP A", flow_direction="L->R")
        draw_ramp(dwg, cfg, x0=110, y0=70, label="RAMP B", flow_direction="R->L")
    
    add_common(dwg)
    dwg.save()
    return output


def draw_sheet_04_ramp_c(cfg: SpecConfig) -> Path:
    output = get_svg_output_path(cfg, "sheet_04_ramp_c.svg")
    dwg = create_drawing(output, "Sheet 04 - Ramp C")
    dwg.add(dwg.text("GEOMETRIC DEVELOPMENT (v002): accordion/stepped profile.", insert=(10, 16), **TEXT_STYLE))
    dwg.add(
        dwg.text(
            f"Pitch p={int(cfg.tread)}mm, rise h={cfg.rise:.1f}mm, modules={cfg.modules}.",
            insert=(10, 22),
            **TEXT_STYLE,
        )
    )
    dwg.add(dwg.text("Horizontal folds alternate M/V from BACK TAB hinge (red then blue...).", insert=(10, 28), **TEXT_STYLE))
    dwg.add(dwg.text("Flow direction: RAMP C L->R (toward exit).", insert=(10, 34), **TEXT_STYLE))
    draw_ramp_3d_example(dwg, x=148, y=13)
    
    if cfg.output_mode == "beginner":
        # Beginner mode: draw RAMP B and C on this sheet (A was on Sheet 03)
        dwg.add(dwg.text("RAMP B (same folding as Ramp A):", insert=(10, 50), **TEXT_STYLE))
        draw_ramp(dwg, cfg, x0=20, y0=60, label="RAMP B", flow_direction="R->L")
        dwg.add(dwg.text("RAMP C (same folding as Ramp A & B):", insert=(10, 170), **TEXT_STYLE))
        draw_ramp(dwg, cfg, x0=20, y0=180, label="RAMP C", flow_direction="L->R")
    else:
        # Standard mode: just Ramp C
        draw_ramp(dwg, cfg, x0=66, y0=90, label="RAMP C", flow_direction="L->R")
    
    add_common(dwg)
    dwg.save()
    return output


def draw_sheet_05_base_tray(cfg: SpecConfig) -> Path:
    output = get_svg_output_path(cfg, "sheet_05_base_tray.svg")
    dwg = create_drawing(output, "Sheet 05 - Base Tray")
    x0, y0 = 45, 95
    floor_w = min(cfg.tray_floor_w, cfg.tray_floor_h)
    floor_h = max(cfg.tray_floor_w, cfg.tray_floor_h)
    wall_h = cfg.tray_wall_h
    front_lip_h = 10.0
    flap_w, flap_h = cfg.tray_flap_w, cfg.tray_flap_h

    dwg.add(dwg.text("Parts: I floor, J side walls, K back wall, L front lip", insert=(10, 16), **TEXT_STYLE))

    # Major tray pieces
    add_rect(dwg, x0, y0, floor_w, floor_h, CUT_STYLE)
    add_rect(dwg, x0, y0 - front_lip_h, floor_w, front_lip_h, CUT_STYLE)
    add_rect(dwg, x0, y0 + floor_h, floor_w, wall_h, CUT_STYLE)
    add_rect(dwg, x0 - wall_h, y0, wall_h, floor_h, CUT_STYLE)
    add_rect(dwg, x0 + floor_w, y0, wall_h, floor_h, CUT_STYLE)

    # Corner glue tabs
    tab_w = 10.0
    for tx, ty, tw, th in [
        (x0 - tab_w, y0 - front_lip_h, tab_w, front_lip_h),
        (x0 + floor_w, y0 - front_lip_h, tab_w, front_lip_h),
        (x0 - tab_w, y0 + floor_h, tab_w, wall_h),
        (x0 + floor_w, y0 + floor_h, tab_w, wall_h),
    ]:
        dwg.add(dwg.rect(insert=(tx, ty), size=(tw, th), fill=GLUE_TAB_FILL, stroke="none"))
        add_rect(dwg, tx, ty, tw, th, CUT_STYLE)

    # Rear flap
    dwg.add(
        dwg.rect(
            insert=(x0 + (floor_w - flap_w) / 2, y0 + floor_h + wall_h),
            size=(flap_w, flap_h),
            fill=GLUE_TAB_FILL,
            stroke="none",
        )
    )
    add_rect(dwg, x0 + (floor_w - flap_w) / 2, y0 + floor_h + wall_h, flap_w, flap_h, CUT_STYLE)

    # Fold lines
    dwg.add(dwg.line(start=(x0, y0), end=(x0 + floor_w, y0), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0, y0 + floor_h), end=(x0 + floor_w, y0 + floor_h), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0, y0), end=(x0, y0 + floor_h), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0 + floor_w, y0), end=(x0 + floor_w, y0 + floor_h), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0, y0 - front_lip_h), end=(x0, y0), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0 + floor_w, y0 - front_lip_h), end=(x0 + floor_w, y0), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0, y0 + floor_h), end=(x0, y0 + floor_h + wall_h), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0 + floor_w, y0 + floor_h), end=(x0 + floor_w, y0 + floor_h + wall_h), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0 + (floor_w - flap_w) / 2, y0 + floor_h + wall_h), end=(x0 + (floor_w - flap_w) / 2 + flap_w, y0 + floor_h + wall_h), **MOUNTAIN_STYLE))

    dwg.add(dwg.text("F1", insert=(x0 + floor_w / 2 - 7, y0 - 1.5), **TEXT_STYLE))
    dwg.add(dwg.text("F2", insert=(x0 + floor_w / 2 - 7, y0 + floor_h - 1.5), **TEXT_STYLE))
    dwg.add(dwg.text("F3", insert=(x0 + 1.2, y0 + 10), **TEXT_STYLE))
    dwg.add(dwg.text("F4", insert=(x0 + floor_w + 1.2, y0 + 10), **TEXT_STYLE))
    dwg.add(dwg.text("F5(M)", insert=(x0 + floor_w / 2 - 7, y0 + floor_h + wall_h - 1.5), **TEXT_STYLE))

    # Labels and short instructions
    dwg.add(dwg.text("I - TRAY FLOOR", insert=(x0 + floor_w / 2 - 18, y0 + floor_h / 2), **TEXT_STYLE))
    dwg.add(dwg.text("L - FRONT LIP (LOW)", insert=(x0 + floor_w / 2 - 19, y0 - 3), **TEXT_STYLE))
    dwg.add(dwg.text("K - BACK WALL", insert=(x0 + floor_w / 2 - 20, y0 + floor_h + 14), **TEXT_STYLE))
    dwg.add(
        dwg.text(
            "J - SIDE WALL",
            insert=(x0 - 16, y0 + floor_h / 2 + 7),
            transform=f"rotate(-90 {x0 - 16} {y0 + floor_h / 2 + 7})",
            **TEXT_STYLE,
        )
    )
    dwg.add(
        dwg.text(
            "J - SIDE WALL",
            insert=(x0 + floor_w + 14, y0 + floor_h / 2 + 7),
            transform=f"rotate(-90 {x0 + floor_w + 14} {y0 + floor_h / 2 + 7})",
            **TEXT_STYLE,
        )
    )
    dwg.add(
        dwg.text(
            "GLUE FLAP (TO REAR / COLLAR ZONE)",
            insert=(x0 + (floor_w - flap_w) / 2 + 12, y0 + floor_h + wall_h + 12),
            **TEXT_STYLE,
        )
    )

    dwg.add(dwg.text("ASSEMBLY (Sheet 05 only):", insert=(10, 28), **TEXT_STYLE))
    dwg.add(dwg.text("1) SCORE F1/F2/F3/F4/F5(M).", insert=(10, 34), **TEXT_STYLE))
    dwg.add(dwg.text("2) FOLD F1-F4 inward to 90° (valley).", insert=(10, 40), **TEXT_STYLE))
    dwg.add(dwg.text("3) FOLD F5(M) as mountain, then glue rear flap.", insert=(10, 46), **TEXT_STYLE))
    dwg.add(dwg.text("4) Glue 4 gray corner tabs inside side walls J.", insert=(10, 52), **TEXT_STYLE))
    dwg.add(dwg.text("5) Keep FRONT LIP toward dice exit side.", insert=(10, 58), **TEXT_STYLE))
    dwg.add(dwg.text("6) BLACK SOLID lines = CUT ONLY.", insert=(10, 64), **TEXT_STYLE))

    dwg.add(dwg.text("NOTE: If BLUE touches BLACK edge, treat it as FOLD line.", insert=(10, 258), **TEXT_STYLE))
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
