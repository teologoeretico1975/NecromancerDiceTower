#!/usr/bin/env python3
"""Generate standard SVG sheets for the Necromancer Dice Tower."""

from agent_02b_svg_generator import (
    build_config_from_specs,
    specs_in_version_order,
    draw_sheet_01_body_a,
    draw_sheet_02_body_b,
    draw_sheet_03_ramps_ab,
    draw_sheet_04_ramp_c,
    draw_sheet_05_base_tray,
    draw_sheet_06_instructions,
    SVG_DIR,
)


def generate_all_modes():
    """Generate sheets in standard mode."""
    spec_paths = specs_in_version_order()
    cfg = build_config_from_specs(spec_paths)

    sheets = [
        ("Sheet 01 (Body A)", draw_sheet_01_body_a),
        ("Sheet 02 (Body B)", draw_sheet_02_body_b),
        ("Sheet 03 (Ramps A/B)", draw_sheet_03_ramps_ab),
        ("Sheet 04 (Ramp C)", draw_sheet_04_ramp_c),
        ("Sheet 05 (Base Tray)", draw_sheet_05_base_tray),
        ("Sheet 06 (Instructions)", draw_sheet_06_instructions),
    ]

    print("\n=== Generating STANDARD mode ===")

    for sheet_name, draw_func in sheets:
        output_path = draw_func(cfg)
        print(f"  ✓ Generated {sheet_name}: {output_path.name}")

    print("\n=== All sheets generated successfully ===")
    print(f"SVG output directory: {SVG_DIR}")
    print("\nFiles created:")
    print("  Standard mode: sheet_01_body_a.svg, sheet_02_body_b.svg, etc.")


if __name__ == "__main__":
    generate_all_modes()
