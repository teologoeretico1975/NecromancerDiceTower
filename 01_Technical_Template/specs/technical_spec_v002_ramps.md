# Necromancer Dice Tower - Technical Specification v002 (Ramps Addendum)

**Last Updated:** 2026-05-22
**Status:** Dual-Mode Output (Standard + Beginner) implemented with UX enhancements

## Purpose

This addendum upgrades the ramp system from v001 smooth ramps to controlled stepped/accordion ramps,
with repeatable assembly behavior and improved rolling reliability for d4 and d6.

This file does not replace v001 entirely. It overrides only ramp-related requirements and
all dependent guide/assembly/test rules.

---

## Dual-Mode Output (2026-05-22 Update)

All v002 ramp sheets are now available in **two variants**:

### Standard Mode
- File: `sheet_03_ramps_ab.svg`, `sheet_04_ramp_c.svg`
- Layout: Compact side-by-side (Sheet 03: Ramps A+B)
- Annotations: Fold IDs, geometric specs, minimal visual guidance
- Audience: Experienced folders, engineers, technical reference

### Beginner Mode
- File: `sheet_03_ramps_ab_beginner.svg`, `sheet_04_ramp_c_beginner.svg`
- Layout: Reorganized for clarity (Sheet 03: Large fold guide + Ramp A; Sheet 04: Ramps B+C)
- Annotations: **Large 1-2-3 visual fold sequence** (y=45–100 mm) showing:
  - **Stage 1 (FLAT):** Unfolded ramp net with all components labeled
  - **Stage 2 (SCORE & FOLD):** Shows blue dashed valley folds and red dotted mountain folds with explanatory arrows
  - **Stage 3 (GLUE & DONE):** Final 3D accordion shape with glue tabs highlighted
- Font sizes: 5px headings, 3.5px detail text (readable for ages 7-10+)
- Additional guidance: "Fold at BACK TAB first", valley/mountain fold reminders
- Audience: First-time builders, children, visual learners

**UX Improvements (2026-05-22):**
- Fold-sequence diagrams moved to top of page (y=45), dedicated space
- Removed text overlap (previously cramped at y=168 on body ramps)
- Beginner mode ramps grouped for cognitive clarity: follow 1-2-3 guide once, apply to all 3 ramps
- Standard mode unchanged for experienced users

Note: dual-mode guidance in this addendum is historical; active technical workflow is now maintained in current single-mode templates/specs.

---

## Scope Changes vs v001

Replace v001 ramp definition with one of the two controlled profiles below:

1. Stepped ramp profile (recommended default for v002)
2. Accordion ramp profile (alternative variant)

In both cases, keep:
- 3 internal ramps (A/B/C)
- alternating directions (A L->R, B R->L, C L->R)
- target body dimensions from v001 unless otherwise revised

Current compatibility baseline (must be preserved in v002 updates):
- Tower shaft footprint: 65 x 65 mm
- Base tray floor: 100 x 130 mm (Sheet 5)
- Effective visible tray terrace target: ~65 mm in front of tower footprint

---

## New Ramp Geometry Requirements

### 1) Stepped Profile (Default, Current Implementation)

Each ramp is made of repeated modules:
- Tread depth p (horizontal segment)
- Rise h (vertical step)

Equivalent slope angle:

tan(theta) = h / p

Recommended starting values for v002 (currently implemented):

| Parameter | Value |
|---|---:|
| Ramp clear width | 56-58 mm |
| Ramp effective run length | 76-86 mm |
| Tread p | **8 mm** |
| Rise h | **3.0 mm** |
| Number of modules per ramp | **8** |
| Side tabs | 8 mm |
| Back tab | 8 mm |
| Side wall height on ramp | 5 mm |

With p=8 and h=3, equivalent angle is about 20.6 deg.

Note:
- This lower equivalent angle is acceptable because step impacts increase die agitation.
- If d4 stalls, test p=7 mm and h=3.5 mm on Ramp B/C only.

### 2) Accordion Profile (Alternative)

Each ramp uses alternating valley/mountain folds to create a corrugated path.

Recommended starting values for v002:

| Parameter | Value |
|---|---:|
| Ramp clear width | 56-58 mm |
| Ramp effective run length | 76-86 mm |
| Fold pitch | 6-7 mm |
| Fold depth (peak-to-valley) | 4-5 mm |
| Number of corrugations | 10-12 |
| Side tabs | 8 mm |
| Back tab | 8 mm |
| Side wall height on ramp | 5 mm |

---

## Clearance and Anti-Jam Constraints

Mandatory constraints for both profiles:

- Minimum clear width for die path: 54 mm.
- Ramp side walls required: 4-6 mm height.
- No pinch points below 8 mm near transitions.
- Entry and exit edges of each ramp must have corner relief (radius or chamfer) >= 1.5 mm.
- Landing zone before each direction change: 8-12 mm nominal flat area.

Dice-specific checks:
- d4 should not wedge between side wall and next ramp edge.
- d6 should not bounce out of ramp side walls.

---

## Sheet 1 and Sheet 2 Guide System (Mandatory Update)

v001 horizontal guides are not sufficient for repeatable slope setup.

Replace each single guide line with two anchor marks per ramp:
- Left anchor: A-L, B-L, C-L
- Right anchor: A-R, B-R, C-R

Each anchor must include a vertical position label in mm from bottom edge.

Target anchors from body bottom (y_bottom):

| Ramp | Left Anchor | Right Anchor | Direction |
|---|---:|---:|---|
| A | 150 mm | 140 mm | L->R |
| B | 90 mm | 100 mm | R->L |
| C | 50 mm | 40 mm | L->R toward exit |

Implementation note:
- Use short guide ticks (not long full lines), so assembler is forced to align by anchors.
- Keep guide styling in the same .guide/.fold classes as technical sheets.
- Keep fold-line IDs (`F1`, `F2`, `F3`) concise and non-overlapping with anchor labels.
- Instructional text on technical sheets defaults to English for international release.
- For tray sheet conventions inherited from v001 updates, allow fold IDs with suffix `(M)` to mark mountain folds (example: `F5(M)`).

---

## Sheet 3 Ramp Net Requirements (Mandatory Update, Now with Beginner Variants)

For each ramp (A/B/C), include:

- Explicit fold map for stepped or accordion pattern.
- Direction label: "HIGH SIDE" and "LOW SIDE".
- Wall glue labels on both sides.
- Back tab label.
- Orientation arrow toward dice flow.

Required labels:
- RAMP A / RAMP B / RAMP C
- HIGH SIDE
- LOW SIDE
- GLUE TO WALL
- FLOW ->

**Beginner Mode Additions (Sheet 03 only):**
- Large 1-2-3 fold sequence visual guide at top (y=45–100 mm)
- Explicit color coding: blue dashed = valley folds, red dotted = mountain folds
- Stage diagrams with flow arrows for left-to-right progression
- Summary text: "Fold at BACK TAB first", fold terminology explained

Localized variants (Italian or bilingual) may be provided as alternate exports; the default technical release remains English.

---

## Material and Rigidity Requirements

Because stepped/accordion ramps can sag, apply one of:

1. Double-layer ramp surface (laminated fold-and-glue), or
2. Rear stiffener rib (folded beam along ramp length)

Cardstock recommendation for v002 ramps:
- Preferred: 220-250 gsm
- Minimum accepted for test: 200 gsm

Reject criteria:
- Visible ramp sag > 3 mm at mid-span under static load of one d20.

---

## Assembly Sequence Changes

Insert these changes into assembly order:

1. Pre-shape each ramp profile before inserting into body.
   - **Beginner Mode:** Follow the 1-2-3 visual guide on Sheet 03 to correctly fold the stepped/accordion profile.
   - **Standard Mode:** Use the geometric development notes at the top of the sheet (pitch/rise/modules).
2. Dry-fit each ramp using anchor marks on both walls.
3. Verify HIGH SIDE and LOW SIDE orientation.
4. Glue only one side first; verify flow; then glue opposite side.
5. Keep 8-12 mm landing zone before next ramp edge.

---

## Test Plan Additions (v002)

Add quantitative dice-flow tests:

| Die | Rolls | Success Exit Target | Max Jam Rate |
|---|---:|---:|---:|
| d4 | 50 | >= 92% | <= 8% |
| d6 | 50 | >= 96% | <= 4% |
| d8 | 30 | >= 95% | <= 5% |
| d10 | 30 | >= 95% | <= 5% |
| d12 | 30 | >= 95% | <= 5% |
| d20 | 30 | >= 95% | <= 5% |

Additional acceptance checks:
- At least 2 direction changes are observed before exit for >= 80% of d6 rolls.
- No persistent jam hotspot in the same position for more than 2/50 d4 rolls.

---

## Acceptance Criteria Override for v002

Replace v001 dice-flow acceptance with:

- Overall success exit rate >= 95% across all tested dice.
- d4 success exit rate >= 92%.
- No structural deformation of ramps after 200 total rolls.
- Assembly repeatability: two independent builds must remain within target jam thresholds.

---

## Deliverables for Template Update (Current Status)

Implemented (2026-05-22):

1. ✓ Sheet 1 SVG: anchor system with A-L/A-R, B-L/B-R, C-L/C-R labels
2. ✓ Sheet 2 SVG: same anchor system and fold ID updates
3. ✓ Sheet 3 SVG: stepped fold map, orientation labels, flow directions
4. ✓ Sheet 4 SVG: Ramp C with v002 compliance
5. ✓ Dual-mode output: Standard (compact) + Beginner (large 1-2-3 visual guide)
6. ✓ Build test document: `build_test_v002.md` with quantitative table

File naming (current):
- Standard mode: `sheet_01_body_a.svg`, `sheet_02_body_b.svg`, `sheet_03_ramps_ab.svg`, `sheet_04_ramp_c.svg`
- Beginner mode: `sheet_01_body_a_beginner.svg`, `sheet_02_body_b_beginner.svg`, `sheet_03_ramps_ab_beginner.svg`, `sheet_04_ramp_c_beginner.svg`
- Ramp build test: `build_test_v002.md`

All formats available: SVG (editable) + PDF (ready to print)

---

## Document History

- **v002.0:** Initial ramp system upgrade with stepped/accordion profiles and quantitative test plan.
- **v002.0+ (2026-05-22):** Dual-mode output implemented with large 1-2-3 fold sequence visual guides for Beginner mode; UX enhancements for assembly clarity.


Each ramp uses alternating valley/mountain folds to create a corrugated path.

Recommended starting values for v002:

| Parameter | Value |
|---|---:|
| Ramp clear width | 56-58 mm |
| Ramp effective run length | 76-86 mm |
| Fold pitch | 6-7 mm |
| Fold depth (peak-to-valley) | 4-5 mm |
| Number of corrugations | 10-12 |
| Side tabs | 8 mm |
| Back tab | 8 mm |
| Side wall height on ramp | 5 mm |

---

## Clearance and Anti-Jam Constraints

Mandatory constraints for both profiles:

- Minimum clear width for die path: 54 mm.
- Ramp side walls required: 4-6 mm height.
- No pinch points below 8 mm near transitions.
- Entry and exit edges of each ramp must have corner relief (radius or chamfer) >= 1.5 mm.
- Landing zone before each direction change: 8-12 mm nominal flat area.

Dice-specific checks:
- d4 should not wedge between side wall and next ramp edge.
- d6 should not bounce out of ramp side walls.

---

## Sheet 1 and Sheet 2 Guide System (Mandatory Update)

v001 horizontal guides are not sufficient for repeatable slope setup.

Replace each single guide line with two anchor marks per ramp:
- Left anchor: A-L, B-L, C-L
- Right anchor: A-R, B-R, C-R

Each anchor must include a vertical position label in mm from bottom edge.

Target anchors from body bottom (y_bottom):

| Ramp | Left Anchor | Right Anchor | Direction |
|---|---:|---:|---|
| A | 150 mm | 140 mm | L->R |
| B | 90 mm | 100 mm | R->L |
| C | 50 mm | 40 mm | L->R toward exit |

Implementation note:
- Use short guide ticks (not long full lines), so assembler is forced to align by anchors.
- Keep guide styling in the same .guide/.fold classes as technical sheets.
- Keep fold-line IDs (`F1`, `F2`, `F3`) concise and non-overlapping with anchor labels.
- Instructional text on technical sheets defaults to English for international release.
- For tray sheet conventions inherited from v001 updates, allow fold IDs with suffix `(M)` to mark mountain folds (example: `F5(M)`).

---

## Sheet 3 Ramp Net Requirements (Mandatory Update)

For each ramp (A/B/C), include:

- Explicit fold map for stepped or accordion pattern.
- Direction label: "HIGH SIDE" and "LOW SIDE".
- Wall glue labels on both sides.
- Back tab label.
- Orientation arrow toward dice flow.

Required labels:
- RAMP A / RAMP B / RAMP C
- HIGH SIDE
- LOW SIDE
- GLUE TO WALL
- FLOW ->

Localized variants (Italian or bilingual) may be provided as alternate exports; the default technical release remains English.

---

## Material and Rigidity Requirements

Because stepped/accordion ramps can sag, apply one of:

1. Double-layer ramp surface (laminated fold-and-glue), or
2. Rear stiffener rib (folded beam along ramp length)

Cardstock recommendation for v002 ramps:
- Preferred: 220-250 gsm
- Minimum accepted for test: 200 gsm

Reject criteria:
- Visible ramp sag > 3 mm at mid-span under static load of one d20.

---

## Assembly Sequence Changes

Insert these changes into assembly order:

1. Pre-shape each ramp profile before inserting into body.
2. Dry-fit each ramp using anchor marks on both walls.
3. Verify HIGH SIDE and LOW SIDE orientation.
4. Glue only one side first; verify flow; then glue opposite side.
5. Keep 8-12 mm landing zone before next ramp edge.

---

## Test Plan Additions (v002)

Add quantitative dice-flow tests:

| Die | Rolls | Success Exit Target | Max Jam Rate |
|---|---:|---:|---:|
| d4 | 50 | >= 92% | <= 8% |
| d6 | 50 | >= 96% | <= 4% |
| d8 | 30 | >= 95% | <= 5% |
| d10 | 30 | >= 95% | <= 5% |
| d12 | 30 | >= 95% | <= 5% |
| d20 | 30 | >= 95% | <= 5% |

Additional acceptance checks:
- At least 2 direction changes are observed before exit for >= 80% of d6 rolls.
- No persistent jam hotspot in the same position for more than 2/50 d4 rolls.

---

## Acceptance Criteria Override for v002

Replace v001 dice-flow acceptance with:

- Overall success exit rate >= 95% across all tested dice.
- d4 success exit rate >= 92%.
- No structural deformation of ramps after 200 total rolls.
- Assembly repeatability: two independent builds must remain within target jam thresholds.

---

## Deliverables for Template Update

To implement this addendum, update:

1. Sheet 1 SVG: replace long ramp guides with A-L/A-R, B-L/B-R, C-L/C-R anchors.
2. Sheet 2 SVG: same anchor system and labels.
3. Sheet 3 SVG: new stepped/accordion fold map and orientation labels.
4. Build test document: add quantitative table fields for jam hotspots and direction-change count.

File naming for first revision after this addendum:
- sheet_01_body_a.svg (or versioned variant: sheet_01_body_a_v002.svg)
- sheet_02_body_b.svg (or versioned variant: sheet_02_body_b_v002.svg)
- sheet_03_ramps_ab.svg (or versioned variant: sheet_03_ramps_ab_v002.svg)
- sheet_04_ramp_c.svg (or versioned variant: sheet_04_ramp_c_v002.svg)
- build_test_v002.md
