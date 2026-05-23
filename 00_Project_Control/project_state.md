# Project State — Necromancer Dice Tower

## Current Phase
- **Phase:** v004 Baffle Core Migration (Anti-Jam Prototype)
- **Status:** Technical templates updated and exported (7 sheets total, including Sheet 07 isometric reference)

## Completed in Session 10 — Sheet 07 Isometric + External Graphics Prompt (2026-05-23)
- Added new technical visualization sheet:
  - [01_Technical_Template/svg/sheet_07_baffle_isometric.svg](01_Technical_Template/svg/sheet_07_baffle_isometric.svg)
  - [01_Technical_Template/pdf/sheet_07_baffle_isometric.pdf](01_Technical_Template/pdf/sheet_07_baffle_isometric.pdf)
- Updated automatic generation flow in [generate_dual_output.py](generate_dual_output.py) to include Sheet 07.
- Added external graphics prompt reference file for DALL·E / Midjourney / SDXL:
  - [00_Project_Control/prompts/sheet_07_external_graphics_prompt.md](00_Project_Control/prompts/sheet_07_external_graphics_prompt.md)
- Verified successful SVG/PDF generation and export for updated technical set.

## Completed in Session 9 — v004 Baffle Core Conversion (2026-05-23)
- **Problem from physical prototype:** internal ramps reduced clearance and caused die jams.
- **Implemented architecture change:** replaced ramp workflow with baffle core workflow.
  - Sheet 03 repurposed to **B1/B2 bulkheads** (alternating mirrored windows)
  - Sheet 04 repurposed to **D1..D6 deflector fins** (staggered wall placement)
  - Sheet 06 instructions rewritten for baffle assembly and anti-jam QA
- **New technical specification:** [01_Technical_Template/specs/technical_spec_v004_baffle_core.md](01_Technical_Template/specs/technical_spec_v004_baffle_core.md)
- **Validation targets added:** center channel >= 30 mm, d6 >=95% exit, d20 >=90% exit

## Completed in Session 8 — Sheet 06 Optimization & Mode Simplification (2026-05-23)
- **Problem**: Sheet 06 assembly instructions had critical readability issues:
  - Section A: Title and text exceeded A4 printable area (overflowed off page)
  - Section D: Materials & tools text overlapped due to cramped layout
  - Font sizing mismatch: 10pt unit was invalid in SVG context, rendered ~14-16px actual
- **Solution implemented**:
  1. **Layout restructuring**: Converted multi-stage horizontal layout → single-column 4-box structure (A/B/C/D sections)
  2. **Font unit correction**: Replaced invalid `10pt` → compact `3.0px` body, `4.6px` heading text
  3. **Explicit wrapping**: Added word-wrap logic (max 92 chars per line) to eliminate overlaps
  4. **Legend scaling**: Reduced from scale 0.72 → 0.58 to fit within reduced vertical footprint
  5. **Micro-tuning**: Compressed line height: 4.0px → 3.8px for better density control
- **Code improvements**:
  - Removed dual-mode complexity (output_mode flag eliminated)
  - Simplified path construction: single standard output per sheet
  - Added reusable functions: `draw_wrapped_text()`, `add_legend()` with scale parameter
  - Updated all 6 sheets: consistent 3.0/3.6/4.6px typography across entire technical suite
- **Validation**:
  - All 6 SVG sheets regenerated successfully ✓
  - All PDF exports completed (exit code 0) ✓
  - Grep verification: confirmed 3.0/4.6px sizing, no pt units detected ✓
  - Sheet 06 text now fits within A4 bounds, no overlaps, sections align properly ✓
- **Deliverables**:
  - Updated SVG sheet 06 (and updated sheets 03-05 for consistency)
  - All PDFs re-exported with new layout
  - Changelog updated with two session entries (Session 6 & 7 notes)
  - Commit: d237c2c (27 files changed, removed 5 beginner PDFs, updated all technical sheets)

## Completed in v002
- Merged specification direction and implementation notes into active workflow.
- Added automated preflight checks to validate environment and key dependencies before run.
- Updated development container baseline for consistent Python 3.11 setup.
- Simplified fold guidance on body/tray sheets for readability (`F1/F2/F3`, `F5(M)`), with English-first operational text.
- Expanded Sheet 5 base tray effective terrace for clearer dice landing visibility (tray floor 100 x 130 mm; effective visible terrace ~65 mm).
- Aligned [01_Technical_Template/specs/technical_spec_v001.md](01_Technical_Template/specs/technical_spec_v001.md) to current sheet geometry and actual 5-sheet layout.
- Synchronized [01_Technical_Template/specs/technical_spec_v002_ramps.md](01_Technical_Template/specs/technical_spec_v002_ramps.md) compatibility baseline and deliverable naming with active files.

## Completed in Session 3 — Dual-Mode + UX Fixes
- **Dual-Mode Output Framework**: Generated all 10 technical sheets (5 Standard + 5 Beginner).
  - Standard mode: compact, technical-focused (original sheets).
  - Beginner mode: enhanced guidance for novice builders.
- **Critical UX Fixes** (2026-05-22 afternoon):
  - **Redesigned fold-sequence visualizations**: Enlarged from tiny 20×20 mm cramped boxes → Large STAGE 1/2/3 diagrams with clear visuals
  - **Fixed text overlap**: Moved sequence from y=168 (overlapping ramps) → y=45 (dedicated space above ramps)
  - **Improved readability**: Font sizes 3.6px → 5px headings; added flow arrows, stage labels, summary tips
  - **Sheet layout optimization**: Beginner Sheet 03 now shows fold guide + RAMP A only; Sheet 04 shows RAMP B + C
  - **Reduced cognitive overload**: Removed duplicate explanation text in Beginner ramps (now centralized in fold guide)

## Validation State
- All 7 standard SVG sheets PASS syntax validation ✓
- PDFs: 7 technical sheets generated successfully ✓
- Sheet 06: No text overflow, sections A-D align within A4 bounds ✓
- Sheet 07: Isometric baffle-core references and callouts generated correctly ✓
- Typography: Consistent 3.0px (body) / 3.6px (standard) / 4.6px (heading) sizing ✓
- Legend: Repositioned y=260, scaled 0.58 ✓

## Deliverables (Current)
- **SVG templates** (7 standard sheets): all files in [01_Technical_Template/svg/](01_Technical_Template/svg/)
- **PDF documents** (7 standard sheets): all files in [01_Technical_Template/pdf/](01_Technical_Template/pdf/)
- **Python code** (agent_02b_svg_generator.py): Single-mode output, removed dual-mode complexity
- **Documentation**: Project state updated (this file); changelog in [changelog.md](changelog.md)

## Next Action (Pending)
1. **Physical build test** with all 7 updated technical sheets (verify baffle flow + assembly clarity)
2. **Art direction phase** — move to decorative artwork layer (motifs, color palette, branding)
3. **PDF asset pack preparation** — organize final deliverables for Etsy listing


