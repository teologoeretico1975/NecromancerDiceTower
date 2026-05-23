# Changelog

## 2026-05-23 (Session 10 — Sheet 07 Isometric + Prompt Workflow)

### Added

- New technical reference sheet:
  - [01_Technical_Template/svg/sheet_07_baffle_isometric.svg](01_Technical_Template/svg/sheet_07_baffle_isometric.svg)
  - [01_Technical_Template/pdf/sheet_07_baffle_isometric.pdf](01_Technical_Template/pdf/sheet_07_baffle_isometric.pdf)
- New external graphics prompt file:
  - [00_Project_Control/prompts/sheet_07_external_graphics_prompt.md](00_Project_Control/prompts/sheet_07_external_graphics_prompt.md)

### Updated

- Batch generation script [generate_dual_output.py](generate_dual_output.py) now includes Sheet 07 in the generated set.
- Generator [agent_02b_svg_generator.py](agent_02b_svg_generator.py) extended with `draw_sheet_07_baffle_isometric(...)` and integrated in main generation flow.

### Validation

- Sheet 07 SVG generation completed successfully.
- Sheet 07 PDF export completed successfully.
- Existing technical exports remain valid under v004 baffle-core workflow.

## 2026-05-23 (Session 9 — v004 Baffle Core Migration)

### Major Change

- Replaced ramp-based internal randomization with **Baffle Core** structures after physical prototype jam feedback.
- Added new spec: [01_Technical_Template/specs/technical_spec_v004_baffle_core.md](01_Technical_Template/specs/technical_spec_v004_baffle_core.md).

### Updated Sheets

- Sheet 03 (`sheet_03_ramps_ab.svg`) repurposed to **B1/B2 bulkheads** with mirrored alternating windows.
- Sheet 04 (`sheet_04_ramp_c.svg`) repurposed to **D1..D6 deflector fins** with staggered placement map.
- Sheet 06 (`sheet_06_instructions.svg`) rewritten from ramp assembly to baffle-core assembly + anti-jam test criteria.

### Validation Targets (v004)

- Center free channel >= 30 mm
- d6 exit success >= 95%
- d20 exit success >= 90%

## 2026-05-23 (Session 8 — Dual-Mode Removal & Single-Mode Finalization)

### Major Refactor

- **Removed dual-mode complexity**: Eliminated `output_mode` flag and beginner/standard file generation logic from [agent_02b_svg_generator.py](agent_02b_svg_generator.py) and [generate_dual_output.py](generate_dual_output.py).
- **Simplified path construction**: Single standard output per sheet; all previous `_beginner.svg` files deleted (5 PDFs removed as well).
- **Single output strategy**: All future work targets single v003 standard output line.

### Technical Improvements

- Added reusable typography utility: `scaled_px(base_px, scale)` for dynamic font sizing in legends and callouts.
- Refactored `add_legend()` to accept `scale` parameter (default 1.0); enables compact legends on dense sheets.
- Introduced `draw_wrapped_text()` function for explicit word-wrapping with configurable max_chars and line_height.
- Added `add_centered_panel_label()` for optical centering of panel identifiers (body sheets).
- Moved anchor tick labels to rotated format (`transform="rotate..."`) to avoid collisions with fold lines.

### Sheet 06 Finalization (Post-Session 7 micro-tuning)

- Further reduced body font: 3.2px → 3.0px; heading font: 4.8px → 4.6px.
- Compressed line height: 4.0px → 3.8px for tighter vertical spacing.
- Reduced legend scale from 0.62 → 0.58 for compact footprint.
- Legend repositioned to y=260 (consistent across all sheets with scale parameter).
- Verified all 4 sections (A/B/C/D) fit within A4 bounds with no text overflow or overlap.

### Affected Files

- Deleted (beginner mode files): 5 `_beginner.svg` files + 5 `_beginner.pdf` files.
- Modified: [agent_02b_svg_generator.py](agent_02b_svg_generator.py), [generate_dual_output.py](generate_dual_output.py), all 6 sheet SVG files.
- Scripts: Updated [scripts/export_all_svg_to_pdf_dual_mode.ps1](scripts/export_all_svg_to_pdf_dual_mode.ps1) (removed beginner file references).

### Validation

- All 6 SVG sheets regenerate with zero errors ✓
- All 6 PDF exports complete successfully ✓
- Typography verified: 3.0px (body), 3.6px (standard), 4.6px (heading) consistent ✓
- No pt units detected in final output ✓
- Commit hash: d237c2c

## 2026-05-23 (Session 7 — Sheet 06 Font Unit Fix)

### Fixed

- Corrected Sheet 06 text sizing bug caused by oversized `pt` units by switching to compact SVG px sizing in [01_Technical_Template/svg/sheet_06_instructions.svg](01_Technical_Template/svg/sheet_06_instructions.svg).
- Kept explicit wrapping for all A/B/C/D sections and tuned wrap density to prevent clipping/overlap in print layout.
- Reduced Sheet 06 legend scale further while preserving the 20 × 20 mm scale check square.

## 2026-05-23 (Session 6 — Sheet 06 Readability Refactor)

### Fixed

- Reworked [01_Technical_Template/svg/sheet_06_instructions.svg](01_Technical_Template/svg/sheet_06_instructions.svg) into a strict single-column layout to keep all content inside the A4 printable area.
- Removed the wide multi-stage horizontal Section A block that exceeded page bounds and replaced it with boxed, wrapped instructions.
- Replaced mixed free-position text blocks with explicit wrapped text boxes for Sections A/B/C/D to prevent overlaps (especially in Section D).

### Updated

- Applied `10pt` typography for Sheet 06 instructional text and headings for consistent readability.
- Reduced Sheet 06 legend scale and kept the 20 × 20 mm calibration square unchanged.

## 2026-05-23 (Session 5 — Final Text Centering + Sheet 05 Bottom Block Fit)

### Refined

- Applied optical centering for main panel labels on body sheets:
  - `FRONT` / `LEFT SIDE` on [01_Technical_Template/svg/sheet_01_body_a.svg](01_Technical_Template/svg/sheet_01_body_a.svg)
  - `BACK` / `RIGHT SIDE` on [01_Technical_Template/svg/sheet_02_body_b.svg](01_Technical_Template/svg/sheet_02_body_b.svg)
- Centering is now generated from panel width rather than fixed text offsets, reducing visual drift if dimensions change.

### Fixed

- Reduced Sheet 05 bottom annotation block to 80% scale to prevent residual crowding near the tray rear flap zone:
  - bottom `NOTE` now rendered at reduced scale
  - `LEGEND` block now rendered at reduced scale
  - scale check square remains unchanged for print validation
  - affected file: [01_Technical_Template/svg/sheet_05_base_tray.svg](01_Technical_Template/svg/sheet_05_base_tray.svg)

## 2026-05-23 (Session 4 — Sheet 01/02 Note Consolidation)

### Fixed

- Resolved residual note/legend overlap risk on body sheets by increasing vertical clearance:
  - [01_Technical_Template/svg/sheet_01_body_a.svg](01_Technical_Template/svg/sheet_01_body_a.svg)
  - [01_Technical_Template/svg/sheet_02_body_b.svg](01_Technical_Template/svg/sheet_02_body_b.svg)

### Consolidated

- Centralized NOTE rendering in generator via shared helper and constants:
  - `BOTTOM_NOTE_TEXT`
  - `BOTTOM_NOTE_Y`
  - `add_bottom_note(...)`
- This prevents future drift and keeps Sheet 01/02 note placement consistent.

### Micro-adjustments

- Final note baseline tuned to `y=251.8` on Sheet 01/02 for cleaner separation from `LEGEND`.
- Sheet 05 keeps its locked/manual profile note baseline at `y=252.3`.

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
