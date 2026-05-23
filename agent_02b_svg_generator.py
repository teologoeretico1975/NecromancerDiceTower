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
NOTCH_FILL = "#FF6600"  # Orange – relief notch triangles: CUT & REMOVE
TEXT_STYLE = {"font_size": "3.6px", "font_family": "Arial", "fill": "black"}

BOTTOM_NOTE_TEXT = "NOTE: If BLUE touches BLACK edge, treat it as FOLD line."
BOTTOM_NOTE_Y = 251.8

ROOT_DIR = Path(__file__).resolve().parent
SPECS_DIR = ROOT_DIR / "01_Technical_Template" / "specs"
SVG_DIR = ROOT_DIR / "01_Technical_Template" / "svg"


def get_svg_output_path(base_name: str) -> Path:
    """Construct SVG output path for standard technical output."""
    return SVG_DIR / base_name
    return SVG_DIR / base_name


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


def scaled_px(base_px: float, scale: float = 1.0) -> str:
    return f"{base_px * scale:.2f}px"


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


def add_legend(
    dwg: svgwrite.Drawing,
    x: float = 10,
    y: float | None = None,
    scale: float = 1.0,
) -> None:
    lx = x
    ly = A4_HEIGHT_MM - 38 if y is None else y
    font_size = scaled_px(3.6, scale)
    line_w = 18 * scale
    text_dx = 21 * scale
    row_1 = 4 * scale
    row_2 = 10 * scale
    row_3 = 16 * scale
    row_4 = 20 * scale
    row_5 = 25 * scale
    row_6 = 28 * scale
    row_7 = 33 * scale
    glue_h = 6 * scale

    dwg.add(dwg.text("LEGEND", insert=(lx, ly), font_size=font_size, font_family="Arial", fill="black"))
    dwg.add(dwg.line(start=(lx, ly + row_1), end=(lx + line_w, ly + row_1), **CUT_STYLE))
    dwg.add(dwg.text("CUT", insert=(lx + text_dx, ly + row_1 + scale), font_size=font_size, font_family="Arial", fill="black"))
    dwg.add(dwg.line(start=(lx, ly + row_2), end=(lx + line_w, ly + row_2), **VALLEY_STYLE))
    dwg.add(dwg.text("VALLEY FOLD", insert=(lx + text_dx, ly + row_2 + scale), font_size=font_size, font_family="Arial", fill="black"))
    dwg.add(dwg.line(start=(lx, ly + row_3), end=(lx + line_w, ly + row_3), **MOUNTAIN_STYLE))
    dwg.add(dwg.text("MOUNTAIN FOLD", insert=(lx + text_dx, ly + row_3 + scale), font_size=font_size, font_family="Arial", fill="black"))
    dwg.add(dwg.rect(insert=(lx, ly + row_4), size=(line_w, glue_h), fill=GLUE_TAB_FILL, stroke="none"))
    dwg.add(dwg.text("GLUE TAB", insert=(lx + text_dx, ly + row_5), font_size=font_size, font_family="Arial", fill="black"))
    dwg.add(dwg.polygon(
        points=[(lx, ly + row_6), (lx + line_w, ly + row_6), (lx, ly + row_6 + glue_h)],
        fill=NOTCH_FILL,
        stroke="black",
        stroke_width=0.4 * scale,
    ))
    dwg.add(dwg.text("NOTCH – CUT & REMOVE", insert=(lx + text_dx, ly + row_7), font_size=font_size, font_family="Arial", fill="black"))


def add_common(dwg: svgwrite.Drawing) -> None:
    add_legend(dwg)
    add_scale_square(dwg)


def add_bottom_note(
    dwg: svgwrite.Drawing,
    y: float = BOTTOM_NOTE_Y,
    scale: float = 1.0,
    x: float = 10,
) -> None:
    dwg.add(
        dwg.text(
            BOTTOM_NOTE_TEXT,
            insert=(x, y),
            font_size=scaled_px(3.6, scale),
            font_family="Arial",
            fill="black",
        )
    )


def add_centered_panel_label(
    dwg: svgwrite.Drawing,
    label: str,
    panel_x: float,
    panel_y: float,
    panel_w: float,
    panel_h: float,
) -> None:
    dwg.add(
        dwg.text(
            label,
            insert=(panel_x + panel_w / 2, panel_y + panel_h / 2),
            text_anchor="middle",
            dominant_baseline="middle",
            **TEXT_STYLE,
        )
    )


def draw_text_block(
    dwg: svgwrite.Drawing,
    x: float,
    y: float,
    lines: list[str],
    line_height: float = 4.2,
    font_size: str = "3.6px",
) -> None:
    for idx, line in enumerate(lines):
        dwg.add(dwg.text(line, insert=(x, y + idx * line_height), font_size=font_size, font_family="Arial", fill="black"))


def draw_wrapped_text(
    dwg: svgwrite.Drawing,
    text: str,
    x: float,
    y: float,
    max_chars: int,
    line_height: float = 4.2,
    font_size: str = "3.6px",
) -> float:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        candidate = f"{cur} {word}".strip()
        if len(candidate) <= max_chars:
            cur = candidate
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)

    for idx, line in enumerate(lines):
        dwg.add(dwg.text(line, insert=(x, y + idx * line_height), font_size=font_size, font_family="Arial", fill="black"))

    return y + max(0, len(lines) - 1) * line_height


def draw_anchor_tick(dwg: svgwrite.Drawing, x: float, y: float, label: str, side: str = "left") -> None:
    dwg.add(dwg.line(start=(x - 4, y), end=(x + 4, y), **VALLEY_STYLE))
    if side == "left":
        # Vertical (rotated) labels along left guide edge for readability.
        tx, ty = (x + 8.7, y + 1.4)
        dwg.add(dwg.text(label, insert=(tx, ty), transform=f"rotate(-90 {tx} {ty})", **TEXT_STYLE))
    else:
        # Vertical (rotated) labels along right guide edge for readability.
        tx, ty = (x - 5.1, y + 1.4)
        dwg.add(dwg.text(label, insert=(tx, ty), transform=f"rotate(90 {tx} {ty})", **TEXT_STYLE))


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
    """Draw 1-2-3 visual sequence LARGE and CLEAR: flat, first fold, glued.
    
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
    output = get_svg_output_path("sheet_01_body_a.svg")
    dwg = create_drawing(output, "Sheet 01 - Body Part A")
    x0, y0, h = 20, 30, cfg.panel_h
    tab_w, front_w, left_w = cfg.glue_tab_a, cfg.front_w, cfg.side_w
    dwg.add(dwg.rect(insert=(x0, y0), size=(tab_w, h), fill=GLUE_TAB_FILL, stroke="none"))
    add_rect(dwg, x0, y0, tab_w + front_w + left_w, h, CUT_STYLE)
    dwg.add(dwg.line(start=(x0 + tab_w, y0), end=(x0 + tab_w, y0 + h), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(x0 + tab_w + front_w, y0), end=(x0 + tab_w + front_w, y0 + h), **VALLEY_STYLE))
    # Fold IDs vertical to avoid collisions with top guidance text.
    f1x, f1y = (x0 + tab_w + 4.4, y0 + 9.0)
    f2x, f2y = (x0 + tab_w + front_w + 4.4, y0 + 9.0)
    dwg.add(dwg.text("F1", insert=(f1x, f1y), transform=f"rotate(-90 {f1x} {f1y})", **TEXT_STYLE))
    dwg.add(dwg.text("F2", insert=(f2x, f2y), transform=f"rotate(-90 {f2x} {f2y})", **TEXT_STYLE))
    add_rotated_tab_label(dwg, "GLUE TAB", x0 + tab_w / 2, y0 + h / 2, -90)
    add_centered_panel_label(dwg, "FRONT", x0 + tab_w, y0, front_w, h)
    add_centered_panel_label(dwg, "LEFT SIDE", x0 + tab_w + front_w, y0, left_w, h)

    # Front dice-exit arch (cut opening) requested for Sheet 01 FRONT panel.
    # Low gothic arch, centered on FRONT panel.
    arch_w = 45.0
    arch_h = 22.0
    front_cx = x0 + tab_w + front_w / 2
    sill_y = y0 + h - 12.0
    arch_left = front_cx - arch_w / 2
    arch_right = front_cx + arch_w / 2
    arch_apex_y = sill_y - arch_h
    arch_path = (
        f"M {arch_left},{sill_y} "
        f"Q {front_cx},{arch_apex_y} {arch_right},{sill_y} "
        f"L {arch_left},{sill_y} Z"
    )
    dwg.add(dwg.path(d=arch_path, **CUT_STYLE))

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
            draw_anchor_tick(dwg, x, y, f"{label} {int(y_from_bottom)}mm", side="left" if label.endswith("-L") else "right")

    dwg.add(dwg.text("FOLD GUIDE:", insert=(10, 16.8), **TEXT_STYLE))
    draw_text_block(
        dwg,
        x=35.8,
        y=16.7,
        lines=[
            "1) SCORE BLUE DASHED lines (F1/F2).",
            "2) FOLD F1/F2 inward to 90°.",
            "3) BLACK SOLID lines = CUT ONLY.",
        ],
        line_height=4.2,
        font_size="3.38px",
    )
    add_bottom_note(dwg)

    add_common(dwg)
    dwg.save()
    return output


def draw_sheet_02_body_b(cfg: SpecConfig) -> Path:
    output = get_svg_output_path("sheet_02_body_b.svg")
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
    # Fold IDs vertical to keep top band clear.
    f1x, f1y = (x0 + tab_a_w + 4.4, y0 + 9.0)
    f2x, f2y = (x0 + tab_a_w + back_w + 4.4, y0 + 9.0)
    dwg.add(dwg.text("F1", insert=(f1x, f1y), transform=f"rotate(-90 {f1x} {f1y})", **TEXT_STYLE))
    dwg.add(dwg.text("F2", insert=(f2x, f2y), transform=f"rotate(-90 {f2x} {f2y})", **TEXT_STYLE))
    dwg.add(dwg.text("F3", insert=(x0 + tab_a_w + back_w + right_w + 1.6, y0 + 9.0), **TEXT_STYLE))
    add_rotated_tab_label(dwg, "GLUE TAB A", x0 + tab_a_w / 2, y0 + h / 2, -90)
    add_centered_panel_label(dwg, "BACK", x0 + tab_a_w, y0, back_w, h)
    add_centered_panel_label(dwg, "RIGHT SIDE", x0 + tab_a_w + back_w, y0, right_w, h)
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
            draw_anchor_tick(dwg, x, y, f"{label} {int(y_from_bottom)}mm", side="left" if label.endswith("-L") else "right")

    dwg.add(dwg.text("FOLD GUIDE:", insert=(9.4, 15.2), **TEXT_STYLE))
    draw_text_block(
        dwg,
        x=35.0,
        y=15.2,
        lines=[
            "1) SCORE BLUE DASHED lines (F1/F2/F3).",
            "2) FOLD F1/F2/F3 inward to 90°.",
            "3) BLACK SOLID lines = CUT ONLY.",
        ],
        line_height=4.2,
        font_size="3.38px",
    )
    add_bottom_note(dwg)

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
    callout_scale: float = 1.0,
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

        # 45° relief notch triangles at every fold junction within side-wall strips.
        # Leg size = rise (h). Notches point toward LOW side (downward, +y direction).
        # Left side-wall strip notches
        for i in range(1, cfg.modules):
            step_y = y0 + min(i * cfg.tread, usable_run)
            # Left notch
            dwg.add(dwg.polygon(
                points=[
                    (x0 + tab_side,               step_y),
                    (x0 + tab_side + cfg.rise,    step_y),
                    (x0 + tab_side,               step_y + cfg.rise),
                ],
                fill=NOTCH_FILL, stroke="black", stroke_width=0.3
            ))
            # Right notch
            dwg.add(dwg.polygon(
                points=[
                    (x0 + tab_side + body_w - cfg.rise,  step_y),
                    (x0 + tab_side + body_w,              step_y),
                    (x0 + tab_side + body_w,              step_y + cfg.rise),
                ],
                fill=NOTCH_FILL, stroke="black", stroke_width=0.3
            ))

        # Minimal geometry hints with controllable scale to avoid overlaps in dense layouts.
        hint_font = f"{3.6 * callout_scale:.2f}px"
        hint_line = 5.0 * callout_scale
        hint_y0 = y0 + body_l + 7
        dwg.add(dwg.text("OUTER BLUE vertical = TAB fold", insert=(x0 + tab_side + 1, hint_y0), font_size=hint_font, font_family="Arial", fill="black"))
        dwg.add(
            dwg.text(
                f"INNER BLUE vertical = SIDE-WALL fold ({int(cfg.side_wall_h)}mm)",
                insert=(x0 + tab_side + 1, hint_y0 + hint_line),
                font_size=hint_font,
                font_family="Arial",
                fill="black",
            )
        )
        dwg.add(dwg.text("ORANGE triangles = NOTCH: CUT & REMOVE before folding", insert=(x0 + tab_side + 1, hint_y0 + 2 * hint_line), font_size=hint_font, font_family="Arial", fill="black"))
    else:
        dwg.add(dwg.text(label, insert=(x0 + tab_side + 20, y0 + 36), **TEXT_STYLE))


def draw_sheet_03_ramps_ab(cfg: SpecConfig) -> Path:
    output = get_svg_output_path("sheet_03_ramps_ab.svg")
    dwg = create_drawing(output, "Sheet 03 - Baffle Core Bulkheads")
    dwg.add(dwg.text("v004 — BAFFLE CORE (BULKHEADS)", insert=(10, 14), font_size="5px", font_family="Arial", font_weight="bold", fill="black"))
    dwg.add(dwg.text("Replace ramps with anti-jam bulkheads. Keep central die channel clear (>=30 mm).", insert=(10, 20), **TEXT_STYLE))

    def draw_bulkhead(x: float, y: float, label: str, top_side: str) -> None:
        tab = 5.0
        body_w = 55.0
        body_h = 120.0
        total_w = tab + body_w + tab

        # Glue tabs
        dwg.add(dwg.rect(insert=(x, y), size=(tab, body_h), fill=GLUE_TAB_FILL, stroke="none"))
        dwg.add(dwg.rect(insert=(x + tab + body_w, y), size=(tab, body_h), fill=GLUE_TAB_FILL, stroke="none"))
        add_rect(dwg, x, y, total_w, body_h, CUT_STYLE)
        dwg.add(dwg.line(start=(x + tab, y), end=(x + tab, y + body_h), **VALLEY_STYLE))
        dwg.add(dwg.line(start=(x + tab + body_w, y), end=(x + tab + body_w, y + body_h), **VALLEY_STYLE))

        # Alternating windows for chicane flow
        win_w = 22.0
        win_h = 16.0
        top_y = y + 20.0
        low_y = y + 74.0
        if top_side == "left":
            top_x = x + tab + 4.0
            low_x = x + tab + body_w - win_w - 4.0
        else:
            top_x = x + tab + body_w - win_w - 4.0
            low_x = x + tab + 4.0
        add_rect(dwg, top_x, top_y, win_w, win_h, CUT_STYLE)
        add_rect(dwg, low_x, low_y, win_w, win_h, CUT_STYLE)

        dwg.add(dwg.text(label, insert=(x + tab + 17, y - 3), font_size="4.2px", font_family="Arial", fill="black", font_weight="bold"))
        dwg.add(dwg.text("GLUE TAB", insert=(x + 0.4, y + body_h + 5), font_size="2.9px", font_family="Arial", fill="black"))
        dwg.add(dwg.text("GLUE TAB", insert=(x + tab + body_w + 0.4, y + body_h + 5), font_size="2.9px", font_family="Arial", fill="black"))

    draw_bulkhead(x=10.0, y=34.0, label="B1 — BULKHEAD", top_side="left")
    draw_bulkhead(x=104.0, y=34.0, label="B2 — BULKHEAD", top_side="right")

    dwg.add(dwg.text("Open windows must alternate left/right between B1 and B2.", insert=(10, 165), font_size="3.2px", font_family="Arial", fill="black"))
    dwg.add(dwg.text("Install B1 above B2 with 25–30 mm vertical gap in final assembly.", insert=(10, 169), font_size="3.2px", font_family="Arial", fill="black"))

    add_common(dwg)
    dwg.save()
    return output


def draw_sheet_04_ramp_c(cfg: SpecConfig) -> Path:
    output = get_svg_output_path("sheet_04_ramp_c.svg")
    dwg = create_drawing(output, "Sheet 04 - Baffle Core Deflectors")
    dwg.add(dwg.text("v004 — BAFFLE CORE (DEFLECTOR FINS)", insert=(10, 14), font_size="5px", font_family="Arial", font_weight="bold", fill="black"))
    dwg.add(dwg.text("Cut 6 fins. Fold on BLUE line. Glue gray tab to inside wall.", insert=(10, 20), **TEXT_STYLE))

    def draw_fin(x: float, y: float, label: str, mirror: bool = False) -> None:
        tab_w = 8.0
        fin_w = 22.0
        fin_h = 18.0
        total_w = tab_w + fin_w

        # Glue tab + fin body
        if mirror:
            dwg.add(dwg.rect(insert=(x + fin_w, y), size=(tab_w, fin_h), fill=GLUE_TAB_FILL, stroke="none"))
            add_rect(dwg, x, y, total_w, fin_h, CUT_STYLE)
            dwg.add(dwg.line(start=(x + fin_w, y), end=(x + fin_w, y + fin_h), **VALLEY_STYLE))
            # Diagonal cut to make fin tip
            dwg.add(dwg.line(start=(x, y + fin_h), end=(x + fin_w, y), **CUT_STYLE))
        else:
            dwg.add(dwg.rect(insert=(x, y), size=(tab_w, fin_h), fill=GLUE_TAB_FILL, stroke="none"))
            add_rect(dwg, x, y, total_w, fin_h, CUT_STYLE)
            dwg.add(dwg.line(start=(x + tab_w, y), end=(x + tab_w, y + fin_h), **VALLEY_STYLE))
            dwg.add(dwg.line(start=(x + tab_w, y), end=(x + total_w, y + fin_h), **CUT_STYLE))

        dwg.add(dwg.text(label, insert=(x, y - 2), font_size="3.1px", font_family="Arial", fill="black"))

    x_positions = [14.0, 72.0, 130.0]
    y_positions = [36.0, 66.0]
    idx = 1
    for row, y in enumerate(y_positions):
        for col, x in enumerate(x_positions):
            mirror = (row + col) % 2 == 1
            draw_fin(x, y, f"D{idx}", mirror=mirror)
            idx += 1

    # Placement map
    dwg.add(dwg.text("PLACEMENT MAP", insert=(10, 112), font_size="4.0px", font_family="Arial", fill="black", font_weight="bold"))
    dwg.add(dwg.text("LEFT WALL: D1, D3, D5 (top to bottom)", insert=(10, 119), font_size="3.4px", font_family="Arial", fill="black"))
    dwg.add(dwg.text("RIGHT WALL: D2, D4, D6 (staggered vs LEFT)", insert=(10, 124), font_size="3.4px", font_family="Arial", fill="black"))
    dwg.add(dwg.text("Fold angle target: 30–45° toward center channel.", insert=(10, 129), font_size="3.4px", font_family="Arial", fill="black"))
    dwg.add(dwg.text("Keep center clear channel >= 30 mm.", insert=(10, 134), font_size="3.4px", font_family="Arial", fill="black"))

    add_common(dwg)
    dwg.save()
    return output


def draw_sheet_06_instructions(cfg: SpecConfig) -> Path:
    """Dedicated instruction sheet for baffle-core folding and assembly."""
    output = get_svg_output_path("sheet_06_instructions.svg")
    dwg = create_drawing(output, "Sheet 06 - Assembly Instructions")

    body_font = "3.0px"
    heading_font = "4.6px"
    line_h = 3.8
    box_x = 10
    box_w = 190

    def add_box(y: float, h: float) -> None:
        dwg.add(dwg.rect(insert=(box_x, y), size=(box_w, h), fill="none", stroke="#cccccc", stroke_width=0.4))

    # Header (wrapped)
    dwg.add(dwg.text("NECROMANCER DICE TOWER — BAFFLE CORE GUIDE", insert=(10, 14), font_size=heading_font, font_family="Arial", font_weight="bold", fill="black"))
    draw_wrapped_text(
        dwg,
        text="Print at 100% on 200–300 gsm cardstock. Score all fold lines before folding.",
        x=10,
        y=20,
        max_chars=92,
        line_height=line_h,
        font_size=body_font,
    )

    # Section A
    a_y = 32
    a_h = 52
    add_box(a_y, a_h)
    dwg.add(dwg.text("A — PREPARE BULKHEADS (B1/B2)", insert=(12, a_y + 7), font_size=heading_font, font_family="Arial", font_weight="bold", fill="#222222"))
    a_lines = [
        "1) CUT B1 and B2 on black solid lines.",
        "2) SCORE BLUE lines and fold side glue tabs to 90°.",
        "3) CUT the alternating windows exactly as printed.",
        "4) Keep windows mirrored: B1 top-left, B2 top-right.",
    ]
    a_text = " ".join(a_lines)
    draw_wrapped_text(dwg, a_text, 12, a_y + 14, max_chars=92, line_height=line_h, font_size=body_font)

    # Section B
    b_y = 88
    b_h = 38
    add_box(b_y, b_h)
    dwg.add(dwg.text("B — WHY BAFFLES (ANTI-JAM)", insert=(12, b_y + 7), font_size=heading_font, font_family="Arial", font_weight="bold", fill="#222222"))
    draw_wrapped_text(
        dwg,
        text="Baffles increase random impacts while preserving a wider free channel than stepped ramps. Alternating openings plus staggered fins reduce jams and keep die flow stable.",
        x=12,
        y=b_y + 14,
        max_chars=92,
        line_height=line_h,
        font_size=body_font,
    )

    # Section C
    c_y = 130
    c_h = 86
    add_box(c_y, c_h)
    dwg.add(dwg.text("C — OVERALL ASSEMBLY ORDER", insert=(12, c_y + 7), font_size=heading_font, font_family="Arial", font_weight="bold", fill="#222222"))
    c_steps = [
        "1) Print all sheets at 100% (no fit-to-page).",
        "2) Score all fold lines before cutting.",
        "3) Assemble body A + body B (Sheets 01-02) and keep seam open for insert steps.",
        "4) Assemble base tray (Sheet 05): F1-F4 valley, F5 mountain, glue corners.",
        "5) Install B1 in upper zone and B2 below it with 25-30 mm gap; tabs glue to opposite walls.",
        "6) Install D1-D6 fins on left/right walls, staggered, fold angle 30-45° toward center.",
        "7) Close body seam, attach base tray, verify center channel >=30 mm, run d6 drop test.",
    ]
    draw_wrapped_text(dwg, " ".join(c_steps), 12, c_y + 14, max_chars=92, line_height=line_h, font_size=body_font)

    # Section D
    d_y = 220
    d_h = 30
    add_box(d_y, d_h)
    dwg.add(dwg.text("D — TEST CRITERIA", insert=(12, d_y + 7), font_size=heading_font, font_family="Arial", font_weight="bold", fill="#222222"))
    d_lines = [
        "• Target pass: d6 >=95% exit, d20 >=90% exit, no persistent jam points.",
        "• If jams occur, reduce fin angle or widen center lane before re-test.",
        "• Keep glue beads thin and avoid spill in window/opening zones.",
        "• Recommended cardstock: 200-250 gsm.",
    ]
    draw_wrapped_text(dwg, " ".join(d_lines), 12, d_y + 14, max_chars=92, line_height=line_h, font_size=body_font)

    # Reduced legend + fixed scale square
    add_legend(dwg, y=260, scale=0.58)
    add_scale_square(dwg)
    dwg.save()
    return output


def draw_sheet_07_baffle_isometric(cfg: SpecConfig) -> Path:
    """Isometric assembly reference for baffle fins and bulkheads (Sheet 07)."""
    output = get_svg_output_path("sheet_07_baffle_isometric.svg")
    dwg = create_drawing(output, "Sheet 07 - Baffle Core Isometric Guide")

    # Header
    dwg.add(dwg.text("v004 — 3D ISOMETRIC ASSEMBLY REFERENCE", insert=(10, 15), font_size="4.8px", font_family="Arial", fill="black", font_weight="bold"))
    dwg.add(dwg.text("Visual guide: how to glue bulkheads B1/B2 and stagger fins D1..D6.", insert=(10, 21), font_size="3.2px", font_family="Arial", fill="black"))

    # Isometric tower shell (simplified prism)
    # Front face
    front = [(40, 65), (115, 65), (115, 190), (40, 190)]
    # Right face offset (isometric)
    right = [(115, 65), (155, 85), (155, 210), (115, 190)]
    # Top face
    top = [(40, 65), (115, 65), (155, 85), (80, 85)]

    dwg.add(dwg.polygon(points=front, fill="none", stroke="black", stroke_width=0.6))
    dwg.add(dwg.polygon(points=right, fill="none", stroke="black", stroke_width=0.6))
    dwg.add(dwg.polygon(points=top, fill="none", stroke="black", stroke_width=0.6))

    # Internal bulkheads (semi-transparent look with light gray fill)
    b1 = [(55, 95), (106, 95), (133, 108), (82, 108)]
    b2 = [(58, 132), (109, 132), (136, 146), (85, 146)]
    dwg.add(dwg.polygon(points=b1, fill="#f2f2f2", stroke="black", stroke_width=0.5))
    dwg.add(dwg.polygon(points=b2, fill="#f2f2f2", stroke="black", stroke_width=0.5))

    # Bulkhead windows (alternating)
    dwg.add(dwg.polygon(points=[(63, 98), (76, 98), (101, 110), (88, 110)], fill="white", stroke="black", stroke_width=0.4))
    dwg.add(dwg.polygon(points=[(86, 135), (99, 135), (124, 148), (111, 148)], fill="white", stroke="black", stroke_width=0.4))

    # Deflector fins (orange) - staggered left/right
    fins = [
        [(52, 108), (61, 103), (61, 110)],
        [(124, 118), (133, 122), (124, 126)],
        [(54, 131), (63, 126), (63, 133)],
        [(126, 142), (135, 146), (126, 150)],
        [(56, 154), (65, 149), (65, 156)],
        [(128, 166), (137, 170), (128, 174)],
    ]
    for fin in fins:
        dwg.add(dwg.polygon(points=fin, fill=NOTCH_FILL, stroke="black", stroke_width=0.4))

    # Flow arrow through chicane
    flow_pts = [(66, 90), (92, 104), (79, 117), (106, 132), (92, 145), (118, 160), (104, 176)]
    dwg.add(dwg.polyline(points=flow_pts, fill="none", stroke="#333333", stroke_width=0.8, stroke_dasharray="2,2"))
    dwg.add(dwg.polygon(points=[(104, 176), (101, 173), (108, 172)], fill="#333333", stroke="none"))
    dwg.add(dwg.text("DIE FLOW", insert=(108, 177), font_size="3.0px", font_family="Arial", fill="#333333"))

    # Callouts
    dwg.add(dwg.line(start=(85, 94), end=(168, 60), stroke="black", stroke_width=0.4))
    dwg.add(dwg.text("B1 BULKHEAD (upper)", insert=(170, 60), font_size="3.2px", font_family="Arial", fill="black"))

    dwg.add(dwg.line(start=(94, 132), end=(168, 86), stroke="black", stroke_width=0.4))
    dwg.add(dwg.text("B2 BULKHEAD (lower)", insert=(170, 86), font_size="3.2px", font_family="Arial", fill="black"))

    dwg.add(dwg.line(start=(129, 119), end=(168, 112), stroke="black", stroke_width=0.4))
    dwg.add(dwg.text("D2/D4/D6 fins on RIGHT wall", insert=(170, 112), font_size="3.2px", font_family="Arial", fill="black"))

    dwg.add(dwg.line(start=(61, 130), end=(168, 138), stroke="black", stroke_width=0.4))
    dwg.add(dwg.text("D1/D3/D5 fins on LEFT wall", insert=(170, 138), font_size="3.2px", font_family="Arial", fill="black"))

    # Angle and clearance notes
    dwg.add(dwg.text("Fold fins toward center at 30–45°", insert=(10, 226), font_size="3.4px", font_family="Arial", fill="black"))
    dwg.add(dwg.text("Keep central clear channel >= 30 mm", insert=(10, 231), font_size="3.4px", font_family="Arial", fill="black"))
    dwg.add(dwg.text("Install B1 and B2 with vertical gap 25–30 mm", insert=(10, 236), font_size="3.4px", font_family="Arial", fill="black"))

    # Mini fold exemplar for one fin
    dwg.add(dwg.text("FIN FOLD EXAMPLE", insert=(10, 248), font_size="3.4px", font_family="Arial", fill="black", font_weight="bold"))
    dwg.add(dwg.rect(insert=(10, 252), size=(22, 10), fill=GLUE_TAB_FILL, stroke="black", stroke_width=0.4))
    dwg.add(dwg.line(start=(18, 252), end=(18, 262), **VALLEY_STYLE))
    dwg.add(dwg.line(start=(18, 252), end=(32, 262), **CUT_STYLE))
    dwg.add(dwg.text("BLUE = fold", insert=(36, 258), font_size="2.8px", font_family="Arial", fill="black"))
    dwg.add(dwg.text("BLACK = cut", insert=(36, 262), font_size="2.8px", font_family="Arial", fill="black"))

    add_common(dwg)
    dwg.save()
    return output


def draw_sheet_05_base_tray(cfg: SpecConfig) -> Path:
    output = get_svg_output_path("sheet_05_base_tray.svg")
    dwg = create_drawing(output, "Sheet 05 - Base Tray")
    # Locked readability layout (manual iteration): shift tray cluster right/up for clearer top text band.
    x0, y0 = 62.2, 79.0
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
    dwg.add(dwg.text("L - FRONT LIP (LOW)", insert=(x0 + floor_w / 2 - 19, y0 - 3), font_size="2.88px", font_family="Arial", fill="black"))
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
            font_size="2.88px",
            font_family="Arial",
            fill="black",
        )
    )

    dwg.add(dwg.text("ASSEMBLY (Sheet 05 only):", insert=(10, 28), **TEXT_STYLE))
    dwg.add(dwg.text("1) SCORE F1/F2/F3/F4/F5(M).", insert=(10, 34), **TEXT_STYLE))
    dwg.add(dwg.text("2) FOLD F1-F4 inward to 90° (valley).", insert=(10, 40), **TEXT_STYLE))
    dwg.add(dwg.text("3) FOLD F5(M) as mountain, then glue rear flap.", insert=(10, 46), **TEXT_STYLE))
    dwg.add(dwg.text("4) Glue 4 gray corner tabs inside side walls J.", insert=(10, 52), **TEXT_STYLE))
    dwg.add(dwg.text("5) Keep FRONT LIP toward dice exit side.", insert=(10, 58), **TEXT_STYLE))
    dwg.add(dwg.text("6) BLACK SOLID lines = CUT ONLY.", insert=(10, 64), **TEXT_STYLE))

    add_bottom_note(dwg, y=252.3, scale=0.8)
    add_legend(dwg, scale=0.8)
    add_scale_square(dwg)
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
        lambda: draw_sheet_06_instructions(cfg),
        lambda: draw_sheet_07_baffle_isometric(cfg),
    ]:
        path = gen()
        print(f"Generated: {path}")


if __name__ == "__main__":
    main()
