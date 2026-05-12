# Generate Technical SVG Template v001

You are the Technical SVG Template Agent.

Use these files as context:
- `00_Project_Control/project_state.md`
- `01_Technical_Template/specs/technical_spec_v001.md`
- `01_Technical_Template/specs/necromancer_dice_tower_sheet_01_body_a_v001.svg`
- `01_Technical_Template/specs/necromancer_dice_tower_sheet_02_body_b_v001.svg`
- `01_Technical_Template/specs/necromancer_dice_tower_sheet_03_ramps_v001.svg`
- `01_Technical_Template/specs/necromancer_dice_tower_sheet_04_base_tray_v001.svg`

Task:
Create four A4 SVG files for the first printable papercraft technical prototype.

CRITICAL OUTPUT RULE:
- The files in `01_Technical_Template/specs/` are the canonical reference.
- Recreate the same visual/technical structure used in the specs files.
- Match style, coordinates, labels, title placement, legend placement, and line patterns used in specs.
- The only intended difference is output location (`01_Technical_Template/svg/`).

Create these files:

1. `01_Technical_Template/svg/necromancer_dice_tower_sheet_01_body_a_v001.svg`
2. `01_Technical_Template/svg/necromancer_dice_tower_sheet_02_body_b_v001.svg`
3. `01_Technical_Template/svg/necromancer_dice_tower_sheet_03_ramps_v001.svg`
4. `01_Technical_Template/svg/necromancer_dice_tower_sheet_04_base_tray_v001.svg`

General SVG requirements:
- A4 portrait.
- `width="210mm"`.
- `height="297mm"`.
- `viewBox="0 0 210 297"`.
- Coordinates in millimeters.
- Safe margin rectangle: x=10, y=10, width=190, height=277.
- Scale check square: 20 × 20 mm.
- Include title text.
- Include legend.
- Use CSS classes for:
  - `.cut`
  - `.fold-valley`
  - `.fold-mountain`
  - `.glue`
  - `.guide`
  - `.label`
  - `.small`
  - `.tiny`
  - `.title`

Required CSS style profile (match specs):
- `.cut { fill: none; stroke: #000000; stroke-width: 0.35; }`
- `.fold-valley { fill: none; stroke: #0066cc; stroke-width: 0.35; stroke-dasharray: 3 2; }`
- `.fold-mountain { fill: none; stroke: #cc0000; stroke-width: 0.35; stroke-dasharray: 1 2; }`
- `.guide { fill: none; stroke: #999999; stroke-width: 0.25; stroke-dasharray: 2 2; }`
- `.glue { fill: #eeeeee; stroke: #000000; stroke-width: 0.35; }`
- `.label { font-family: Arial, sans-serif; font-size: 4px; fill: #000000; }`
- `.small { font-family: Arial, sans-serif; font-size: 3px; fill: #000000; }`
- `.tiny { font-family: Arial, sans-serif; font-size: 2.6px; fill: #000000; }`
- `.title { font-family: Arial, sans-serif; font-size: 4.5px; font-weight: bold; fill: #000000; }`

Line style:
- `.cut`: black solid line.
- `.fold-valley`: blue dashed line.
- `.fold-mountain`: red dotted line.
- `.glue`: light gray fill with black stroke.
- `.guide`: gray dashed line.

Title and page framing rules (match specs):
- Include a `<title>` element in the SVG root.
- Place visible title text at x=10, y=7 with class `.title`.
- Keep safe margin as `<rect x="10" y="10" width="190" height="277" class="guide"/>`.
- Scale area and legend must be in lower page area, with the same structure used in specs.

Sheet 1:
Body Part A:
- Front panel: 65 × 190 mm.
- Left side panel: 65 × 190 mm.
- Glue tab: 10 × 190 mm.
- Dice exit on front panel: 50 × 42 mm.
- Exit centered horizontally on front panel.
- Exit bottom margin: 15 mm.
- Add labels: FRONT, LEFT SIDE, GLUE.
- Add ramp guide marks.

Sheet 1 placement/profile guidance from specs:
- Use FRONT at x=25..90, LEFT SIDE at x=90..155, GLUE tab at x=155..165.
- Keep ramp guides and labels exactly in the LEFT SIDE panel region as in specs.
- Use rotated tiny text for GLUE tab labels where present.

Sheet 2:
Body Part B:
- Glue tab: 10 × 190 mm.
- Back panel: 65 × 190 mm.
- Right side panel: 65 × 190 mm.
- Glue tab: 10 × 190 mm.
- Add labels: BACK, RIGHT SIDE, GLUE.
- Add ramp guide marks.

Sheet 2 placement/profile guidance from specs:
- Left glue tab at x=30..40, BACK at x=40..105, RIGHT SIDE at x=105..170, right glue tab at x=170..180.
- Keep ramp guide lines and labels in RIGHT SIDE panel area exactly as in specs.

Sheet 3:
Internal ramps:
- Create three ramp nets: RAMP A, RAMP B, RAMP C.
- Each ramp surface: 58 × 70 mm.
- Side glue tabs: 8 mm.
- Back glue tab: 8 mm.
- Add labels and fold lines.

Sheet 3 placement/profile guidance from specs:
- Follow the same three ramp net layout blocks and coordinate ranges used in specs.
- Include `GLUE TO WALL` and rotated `GLUE` labels like specs.
- Include the two explanatory small text lines near the lower-middle area.

Sheet 4:
Base tray:
- Tray floor: 95 × 90 mm.
- Front wall: 95 × 25 mm.
- Left wall: 90 × 25 mm.
- Right wall: 90 × 25 mm.
- Back connection flap: 65 × 20 mm.
- Glue tabs: 10 mm.
- Add labels.

Sheet 4 placement/profile guidance from specs:
- Use the same net arrangement and coordinate pattern as specs (tray centered, side walls, front wall, top connection flap).
- Include short descriptive notes in the upper-left content area, as in specs.
- Keep vertical wall labels rotated where used in specs.

Important:
- Do not create final decorative fantasy art.
- Do not embed bitmap images.
- Keep SVG clean and readable.
- Prefer simple primitive elements (`rect`, `line`, `text`, `path`, `polygon`) like specs.
- After creating files, verify each generated SVG against its specs counterpart.
- In the final response, report: what was created, whether spec parity was achieved, and what should be tested physically.
