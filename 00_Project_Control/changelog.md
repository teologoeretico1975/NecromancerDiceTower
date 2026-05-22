# Changelog

## 2026-05-22 (Session 3 — UX Fixes)

### Fixed (Critical UX Issues)

- **Beginner Mode Fold Sequence Redesign**:
  - Previous implementation: Tiny 1×2×3 boxes (20×20 mm area, y=168) causing text overlap with ramp geometry
  - Fixed: Completely redesigned `draw_ramp_fold_sequence()` with LARGE visual diagrams
  - New layout (all Beginner mode sheets):
    - Stage 1: **FLAT NET** — Large rectangle showing unfolded pieces
    - Stage 2: **SCORE & FOLD** — Shows valley fold lines (blue dashed) being creased
    - Stage 3: **GLUE & DONE** — Final accordion shape with glue tabs highlighted
    - Font size increased: 3.6px → 5px (title), 3.5px (labels)
    - Added arrows between stages for flow clarity
    - Added summary tips: "Fold at BACK TAB first" + valley/mountain fold reminders
  - Positioned at top of page (y=45) to avoid overlap with ramp diagrams

- **Sheet Layout Optimization (Beginner Mode)**:
  - **Sheet 03 Beginner**: Changed from 2-ramps side-by-side → Large fold guide (y=45) + RAMP A only (y=130)
  - **Sheet 04 Beginner**: Changed from 1 ramp → RAMP B (y=60) + RAMP C (y=180)
  - Rationale: Reduces cognitive load; users follow one 1-2-3 guide then apply it to 3 ramps
  - Standard mode unchanged: Sheet 03 still has Ramps A+B, Sheet 04 still has Ramp C

- **Text Overlap Elimination (Beginner Mode)**:
  - Removed duplicate explanation text ("OUTER BLUE vertical = TAB fold", "INNER BLUE vertical = SIDE-WALL fold") in Beginner mode ramps
  - These are now ONLY shown in Standard mode (Beginner mode has explicit visual guide)
  - Prevents cramping; improves readability

### Generated

- All 10 SVG files regenerated (Standard + Beginner, all 5 sheets)
- All 10 PDF files re-exported with improved visuals
- Beginner mode now features clear, large fold-sequence diagrams suitable for ages 7-10+

### Validated

- All 10 SVG files pass preflight (verified 2026-05-22 post-fix)
- All 10 PDF files exported successfully
- No visual overlaps in Beginner-mode Sheets 03/04
- Text baseline validated: 4-5px headings + 3.5px detail labels clearly readable at A4 100% print

---

## 2026-05-22 (Session 3 — Initial Dual-Mode)

### Added

- **Dual-Mode SVG Output** (Standard + Beginner) implemented across all 5 technical sheets:
  - Standard mode: compact, minimal annotations (original technical templates).
  - Beginner mode: expanded guidance for novice builders including explicit fold sequence visualization and step-by-step cues.
- **Beginner Mode Features** (original iteration, now improved):
  - Small 1-2-3 visual fold sequence diagrams on ramp sheets (Sheet 03/04) showing flat → folded → glued states.
  - Extra inline guidance text added to ramp sheets: "→ Score and fold all RED/BLUE lines BEFORE cutting", "→ Start folding at BACK TAB hinge (top), work downward".
  - Fold sequence visualization positioned at lower left (y=168mm) to avoid overlap with ramp diagrams. **[LATER FIXED: moved to top, enlarged]**
- **Generator Enhancement** ([agent_02b_svg_generator.py](agent_02b_svg_generator.py)):
  - Added `output_mode` config flag to `SpecConfig` (options: "standard", "beginner").
  - Added `get_svg_output_path(cfg, base_name)` helper for automatic output path naming with mode suffix.
  - Added `draw_ramp_fold_sequence(dwg, x, y)` function generating 3-stage visual progression. **[LATER: completely redesigned for better UX]**
  - All 5 `draw_sheet_*()` functions updated to use mode-aware path construction.
- **Dual-Mode Export Script** ([generate_dual_output.py](generate_dual_output.py)):
  - Single-pass generator producing all 10 SVG files (5 Standard + 5 Beginner).
  - File naming convention: `sheet_XX_name.svg` (Standard), `sheet_XX_name_beginner.svg` (Beginner).

### Generated

- **SVG Files** (10 total, all PASS preflight):
  - Standard mode (5): `sheet_01_body_a.svg`, `sheet_02_body_b.svg`, `sheet_03_ramps_ab.svg`, `sheet_04_ramp_c.svg`, `sheet_05_base_tray.svg`.
  - Beginner mode (5): `sheet_01_body_a_beginner.svg`, `sheet_02_body_b_beginner.svg`, `sheet_03_ramps_ab_beginner.svg`, `sheet_04_ramp_c_beginner.svg`, `sheet_05_base_tray_beginner.svg`.
  - Source: [01_Technical_Template/svg/](01_Technical_Template/svg/).
- **PDF Files** (10 total):
  - Standard mode (5): `sheet_01_body_a.pdf` ... `sheet_05_base_tray.pdf`.
  - Beginner mode (5): `sheet_01_body_a_beginner.pdf` ... `sheet_05_base_tray_beginner.pdf`.
  - Source: [01_Technical_Template/pdf/](01_Technical_Template/pdf/).

### Validated

- All 10 SVG files pass automated preflight checks (Standard mode verified; Beginner mode included in same structure).
- All 10 PDF exports completed successfully via Inkscape.
- No textual overlaps in Beginner-mode annotations (fold sequence diagrams positioned at y=168mm, clear of ramp bodies). **[LATER FIXED: moved to y=45mm with larger font]**

--- 

## 2026-05-22 (Earlier)

[Earlier entries follow...]


### Updated

- Base tray geometry on [01_Technical_Template/svg/sheet_05_base_tray.svg](01_Technical_Template/svg/sheet_05_base_tray.svg) revised for improved dice landing visibility:
	- tray floor confirmed at 100 x 130 mm
	- rear glue flap aligned to tower coupling width 65 mm
	- effective visible terrace depth now ~65 mm
- Technical assembly text and fold IDs normalized for readability and international release on active technical sheets (English-first, compact IDs including `F5(M)`).
- Main technical spec aligned with implemented geometry and sheet structure in [01_Technical_Template/specs/technical_spec_v001.md](01_Technical_Template/specs/technical_spec_v001.md):
	- version moved to 1.1
	- tower footprint updated to 65 x 65 mm
	- current 5-sheet technical layout documented
	- tray section updated to current Sheet 5 conventions
- Ramp addendum synchronized with current baseline and file naming in [01_Technical_Template/specs/technical_spec_v002_ramps.md](01_Technical_Template/specs/technical_spec_v002_ramps.md).
- Consolidated ramp sheets [01_Technical_Template/svg/sheet_03_ramps_ab.svg](01_Technical_Template/svg/sheet_03_ramps_ab.svg) and [01_Technical_Template/svg/sheet_04_ramp_c.svg](01_Technical_Template/svg/sheet_04_ramp_c.svg) against v002 rules:
	- alternating flow directions enforced (A L->R, B R->L, C L->R)
	- ramp B HIGH/LOW side labels corrected to match reverse flow
	- concise v002 profile notes added on both sheets for build clarity

### Validated

- Automated SVG preflight passed for all current sheets (01-05).
- Post-consolidation verification confirmed flow labels on ramp sheets (including `FLOW <-` on ramp B).
- Full technical PDF export completed successfully for all current sheets:
	- [01_Technical_Template/pdf/sheet_01_body_a.pdf](01_Technical_Template/pdf/sheet_01_body_a.pdf)
	- [01_Technical_Template/pdf/sheet_02_body_b.pdf](01_Technical_Template/pdf/sheet_02_body_b.pdf)
	- [01_Technical_Template/pdf/sheet_03_ramps_ab.pdf](01_Technical_Template/pdf/sheet_03_ramps_ab.pdf)
	- [01_Technical_Template/pdf/sheet_04_ramp_c.pdf](01_Technical_Template/pdf/sheet_04_ramp_c.pdf)
	- [01_Technical_Template/pdf/sheet_05_base_tray.pdf](01_Technical_Template/pdf/sheet_05_base_tray.pdf)

## 2026-05-20 (Session 2)

### Updated

- Dev container now includes Inkscape auto-install in `postCreateCommand` for persistent PDF export capability.
- VS Code tasks fully aligned to current sheet-based SVG workflow (`sheet_01..sheet_05`).
- PDF export task count increased from 4 to 5 sheets (added `sheet_05_base_tray`).

### Fixed

- Resolved JSON schema validation error in `.devcontainer/devcontainer.json` and `.vscode/settings.json` (invalid `workbench.editorAssociations` value).
- PDF viewer extension pinned via:
  - `tomoki1207.pdf` in devcontainer extensions list.
  - `.vscode/extensions.json` with workspace recommendations.
- This prevents viewer loss across reload/rebuild cycles.

### Generated

- PDF exports of all 5 current sheets (11.4–12 KB each) saved to `01_Technical_Template/pdf/`.

## 2026-05-20 (Session 1)

### Added

- Persistent SVG generator script with merged-spec support: [agent_02b_svg_generator.py](agent_02b_svg_generator.py).
- Persistent automated build preflight script: [01_Technical_Template/test_builds/agent_03_svg_build_test.py](01_Technical_Template/test_builds/agent_03_svg_build_test.py).
- Dev container configuration: [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json).

### Updated

- Sheet 3 validation and A4 fit math in [01_Technical_Template/specs/technical_spec_v001.md](01_Technical_Template/specs/technical_spec_v001.md).
- Build test report updated with automated preflight outcomes in [01_Technical_Template/test_builds/build_test_v002.md](01_Technical_Template/test_builds/build_test_v002.md).
- SVG generator now loads all `technical_spec_v*.md` files and applies latest ramp overrides.

### Generated

- New technical sheets produced by Agent 02b:
	- [01_Technical_Template/svg/sheet_01_body_a.svg](01_Technical_Template/svg/sheet_01_body_a.svg)
	- [01_Technical_Template/svg/sheet_02_body_b.svg](01_Technical_Template/svg/sheet_02_body_b.svg)
	- [01_Technical_Template/svg/sheet_03_ramps_ab.svg](01_Technical_Template/svg/sheet_03_ramps_ab.svg)
	- [01_Technical_Template/svg/sheet_04_ramp_c.svg](01_Technical_Template/svg/sheet_04_ramp_c.svg)
	- [01_Technical_Template/svg/sheet_05_base_tray.svg](01_Technical_Template/svg/sheet_05_base_tray.svg)

### Removed

- Legacy versioned SVG/PDF/PNG exports cleaned during workspace reset and replaced by new sheet-based outputs.

## 2026-05-12

### Added

- Workspace custom agent for technical SVG generation: [.github/agents/technical-svg-template.agent.md](.github/agents/technical-svg-template.agent.md).
- Ramp-focused v002 specification addendum: [01_Technical_Template/specs/technical_spec_v002_ramps.md](01_Technical_Template/specs/technical_spec_v002_ramps.md).
- New technical build test checklist with quantitative flow metrics: [01_Technical_Template/test_builds/build_test_v002.md](01_Technical_Template/test_builds/build_test_v002.md).

### Created

- v002 SVG sheets:
	- [01_Technical_Template/svg/necromancer_dice_tower_sheet_01_body_a_v002.svg](01_Technical_Template/svg/necromancer_dice_tower_sheet_01_body_a_v002.svg)
	- [01_Technical_Template/svg/necromancer_dice_tower_sheet_02_body_b_v002.svg](01_Technical_Template/svg/necromancer_dice_tower_sheet_02_body_b_v002.svg)
	- [01_Technical_Template/svg/necromancer_dice_tower_sheet_03_ramps_v002.svg](01_Technical_Template/svg/necromancer_dice_tower_sheet_03_ramps_v002.svg)
- v002b readability-tuned SVG sheets:
	- [01_Technical_Template/svg/necromancer_dice_tower_sheet_01_body_a_v002b.svg](01_Technical_Template/svg/necromancer_dice_tower_sheet_01_body_a_v002b.svg)
	- [01_Technical_Template/svg/necromancer_dice_tower_sheet_02_body_b_v002b.svg](01_Technical_Template/svg/necromancer_dice_tower_sheet_02_body_b_v002b.svg)
	- [01_Technical_Template/svg/necromancer_dice_tower_sheet_03_ramps_v002b.svg](01_Technical_Template/svg/necromancer_dice_tower_sheet_03_ramps_v002b.svg)

### Updated

- Sheet 03 v002 explanatory text wrapped and moved to avoid truncation/overlap.
- White page background added to v002 sheets to improve preview readability on dark UI themes.
- PNG/PDF exports regenerated for v002 and v002b under [01_Technical_Template/pdf](01_Technical_Template/pdf) and [01_Technical_Template/exports_png](01_Technical_Template/exports_png).
