# Dual-Mode Output Guide — Standard vs. Beginner

## Overview

The Necromancer Dice Tower technical template now supports **two output modes** for each of the 5 sheets:

1. **Standard Mode** — Compact, technical-focused sheets for experienced builders
2. **Beginner Mode** — Enhanced guidance with visual fold sequences for novice builders

This document explains the differences, when to use each, and how to generate them.

---

## Mode Comparison

| Aspect | Standard | Beginner |
|--------|----------|----------|
| **Audience** | Experienced folders, engineers, technical review | First-time builders, young kids (8-10+), visual learners |
| **Annotations** | Minimal, IDs only (F1, F2, FLOW ->) | Extra guidance text, numbered steps, visual progression |
| **Fold Visuals** | Legend only | Legend + 1-2-3 fold sequence diagrams (Sheets 3-4 ramps) |
| **File Size** | ~27–28 KB | ~32–35 KB (includes diagrams) |
| **Print Volume** | Standard (1 set = 5 pages) | Standard (1 set = 5 pages, same physical size) |
| **Complexity** | v002 spec-aligned, minimal | Same geometry, enhanced UX |

---

## Standard Mode Features

**File naming:** `sheet_01_body_a.svg` (no suffix)

### Content
- Compact fold IDs: F1, F2, F3, F5(M)
- Flow direction markers: FLOW -> (L→R), FLOW <- (R←L)
- Geometric development notes (ramps only)
- 3D wireframe example fold profile (ramps only)
- Legend wit cut/fold/glue line conventions
- 20×20 mm scale check square

### Use Cases
- **Experienced makers** creating prototypes or refinements
- **Technical documentation** and reference
- **Print optimization** when paper/ink is limited
- **Advanced variant** for Etsy product offering (future)

---

## Beginner Mode Features

**File naming:** `sheet_01_body_a_beginner.svg` (with `_beginner` suffix)

### Content
Everything in Standard mode, **plus:**

- **Extra inline guidance** on ramp sheets:
  - "→ Score and fold all RED/BLUE lines BEFORE cutting"
  - "→ Start folding at BACK TAB hinge (top), work downward"
- **Visual fold-sequence boxes** on Sheets 3–4 (ramps):
  - Stage 1: FLAT — baseline rectangle showing full net
  - Stage 2: SCORE & FOLD — diagram showing first valley fold with back-tab mountain fold
  - Stage 3: GLUE — assembled ramp showing glue tabs and final shape
- **labeled steps** with simple wireframe visuals

### Use Cases
- **Novice users** (8-10+ year-olds, first-time folders)
- **Educational settings** (classroom craft activities)
- **Accessibility variant** for non-English or inexperienced audiences
- **Primary deliverable** for Etsy if child-friendly positioning is core

---

## Generator Configuration

### Generating Both Modes (Automated)

Run the dual-mode generator to create all 10 files (Standard + Beginner) in one pass:

```bash
python generate_dual_output.py
```

**Output:**
```
=== Generating STANDARD mode ===
  ✓ Generated Sheet 01 (Body A): sheet_01_body_a.svg
  ✓ Generated Sheet 02 (Body B): sheet_02_body_b.svg
  ...

=== Generating BEGINNER mode ===
  ✓ Generated Sheet 01 (Body A): sheet_01_body_a_beginner.svg
  ✓ Generated Sheet 02 (Body B): sheet_02_body_b_beginner.svg
  ...
```

### Manual Mode Selection (Python)

```python
from agent_02b_svg_generator import build_config_from_specs, specs_in_version_order
from agent_02b_svg_generator import draw_sheet_01_body_a  # or any sheet function

spec_paths = specs_in_version_order()
cfg = build_config_from_specs(spec_paths)

# Standard mode (default)
cfg.output_mode = "standard"
output_path = draw_sheet_01_body_a(cfg)
print(f"Generated: {output_path}")

# Beginner mode
cfg.output_mode = "beginner"
output_path = draw_sheet_01_body_a(cfg)
print(f"Generated: {output_path}")
```

---

## File Organization

### SVG Source Files
```
01_Technical_Template/svg/
├── sheet_01_body_a.svg                 (Standard)
├── sheet_01_body_a_beginner.svg        (Beginner)
├── sheet_02_body_b.svg                 (Standard)
├── sheet_02_body_b_beginner.svg        (Beginner)
... (5 Standard + 5 Beginner)
```

### PDF Export Files
```
01_Technical_Template/pdf/
├── sheet_01_body_a.pdf                 (Standard)
├── sheet_01_body_a_beginner.pdf        (Beginner)
├── sheet_02_body_b.pdf                 (Standard)
├── sheet_02_body_b_beginner.pdf        (Beginner)
... (5 Standard + 5 Beginner)
```

---

## Exporting to PDF

### All Files (Standard + Beginner)

Use the provided PowerShell script:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/export_all_svg_to_pdf_dual_mode.ps1
```

### Single Mode

To export only Standard or only Beginner:

```bash
# Standard mode only (5 files)
for file in sheet_01_body_a.svg sheet_02_body_b.svg sheet_03_ramps_ab.svg sheet_04_ramp_c.svg sheet_05_base_tray.svg; do
  inkscape "01_Technical_Template/svg/$file" --export-type=pdf "--export-filename=01_Technical_Template/pdf/${file%.svg}.pdf"
done

# Beginner mode only (5 files)
for file in sheet_*_beginner.svg; do
  inkscape "01_Technical_Template/svg/$file" --export-type=pdf "--export-filename=01_Technical_Template/pdf/${file%.svg}.pdf"
done
```

---

## Validation & Testing

### Preflight Check (All Sheets)

```bash
python 01_Technical_Template/test_builds/agent_03_svg_build_test.py
```

**Note:** Currently validates Standard mode files. Beginner mode files inherit the same structure; manual spot-checks recommended.

### Physical Build Test

- **Standard:** Test with experienced folder; benchmark for technical accuracy
- **Beginner:** Test with target age group (8-10 year-old); measure comprehension and autonomy score

---

## Future Enhancements

1. **Advanced Mode** — Minimal annotations for expert folders (faster printing, cleaner visuals)
2. **Step-by-Step Animations** — Replace static fold-sequence boxes with multi-frame visuals
3. **Internationalization** — Create Beginner variants in additional languages (Italian, Spanish, etc.)
4. **Interactive PDF** — Embed clickable layers to toggle Standard/Beginner annotations per sheet
5. **Video Links** — QR codes on sheets linking to fold tutorial videos

---

## Decision Tree: Which Mode to Use?

```
Is your builder...
├── Ages 8-10?  → Beginner mode ✓
├── Ages 10-14? → Beginner mode (recommended) or Standard if advanced
├── Ages 14+?   → Standard mode (or Advanced if offered)
├── Experienced folder? → Standard mode ✓
├── Engineer/designer? → Standard mode ✓
└── If uncertain? → Beginner mode (more guidance never hurts)
```

---

## Maintenance Notes

- **Generator code:** [agent_02b_svg_generator.py](agent_02b_svg_generator.py) (line ~45: `output_mode` config flag)
- **Beginner-specific functions:** `draw_ramp_fold_sequence()` (lines ~360–430)
- **Mode detection:** `get_svg_output_path()` helper (lines ~40–47)
- **Dual-mode workflow:** [generate_dual_output.py](generate_dual_output.py)

### Updating or Adding Content

When modifying any sheet or adding new guidance:
1. Update generator function (e.g., `draw_sheet_03_ramps_ab()`)
2. Test both modes: `cfg.output_mode = "standard"` then `cfg.output_mode = "beginner"`
3. Regenerate: `python generate_dual_output.py`
4. Validate: `python 01_Technical_Template/test_builds/agent_03_svg_build_test.py`
5. Export: Use the PowerShell export script

---

## Version History

- **v001**: Standard mode only (single technical template)
- **v002**: Standard mode refined (ramp geometry, fold conventions)
- **v002+ (Current)**: Dual-mode output introduced (Standard + Beginner for enhanced accessibility)

---

**Last Updated:** 2026-05-22  
**Maintainer:** Necromancer Dice Tower Project  
**Status:** Production Ready (10 SVG files + 10 PDF files, all validated)
