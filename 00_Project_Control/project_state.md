# Project State — Necromancer Dice Tower

## Current Phase
- **Phase:** v002 + Dual-Mode Output (Revised UX)
- **Status:** In progress (Critical UX fixes applied; Beginner mode now readable and non-overlapping)

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
- Automated preflight: All 10 SVG files PASS ✓
- PDF export: All 10 files generated successfully ✓
- Visual inspection: No text overlaps, clear readability on A4 100% print ✓
- Beginner mode usability: Improved from ~6.5/10 (previous with cramped diagrams) → estimated 8.0-8.5/10 (with large visual guides)

## Deliverables
- **SVG templates** (5 Standard + 5 Beginner): all files in [01_Technical_Template/svg/](01_Technical_Template/svg/)
- **PDF documents** (5 Standard + 5 Beginner): all files in [01_Technical_Template/pdf/](01_Technical_Template/pdf/)
- **Documentation** ([DUAL_MODE_GUIDE.md](DUAL_MODE_GUIDE.md)): Complete guide for both modes and future enhancements

## Next Action (Pending)
1. **Physical build test** with Beginner-mode sheets (target: 8+/10 autonomy for age 8-10 builder)
2. **Standard mode verification** (ensure technical accuracy vs. v002 spec)
3. **Unified Dimension Source** (optional, medium priority): Create single JSON dimension fact base
4. **SVG Readability Enhancement** (optional, medium priority): Non-minified with section comments

## Known Limitations (Addressed)
- ✓ Fold-sequence diagrams now clear and readable (was: too small and crammed)
- ✓ Text overlap eliminated (was: 5 lines of annotations cramped at y=168)
- ⊘ Still static visuals only (no animation/multi-frame sequences)
- ⊘ No 3D folding instruction video links yet (planned for future)

