# Necromancer Dice Tower - Technical Specification v002 (Ramps Addendum)

## Purpose

This addendum upgrades the ramp system from v001 smooth ramps to controlled stepped/accordion ramps,
with repeatable assembly behavior and improved rolling reliability for d4 and d6.

This file does not replace v001 entirely. It overrides only ramp-related requirements and
all dependent guide/assembly/test rules.

---

## Scope Changes vs v001

Replace v001 ramp definition with one of the two controlled profiles below:

1. Stepped ramp profile (recommended default for v002)
2. Accordion ramp profile (alternative variant)

In both cases, keep:
- 3 internal ramps (A/B/C)
- alternating directions (A L->R, B R->L, C L->R)
- target body dimensions from v001 unless otherwise revised

---

## New Ramp Geometry Requirements

## 1) Stepped Profile (Default)

Each ramp is made of repeated modules:
- Tread depth p (horizontal segment)
- Rise h (vertical step)

Equivalent slope angle:

tan(theta) = h / p

Recommended starting values for v002:

| Parameter | Value |
|---|---:|
| Ramp clear width | 56-58 mm |
| Ramp effective run length | 76-86 mm |
| Tread p | 8 mm |
| Rise h | 3 mm |
| Number of modules per ramp | 8 |
| Side tabs | 8 mm |
| Back tab | 8 mm |
| Side wall height on ramp | 5 mm |

With p=8 and h=3, equivalent angle is about 20.6 deg.

Note:
- This lower equivalent angle is acceptable because step impacts increase die agitation.
- If d4 stalls, test p=7 mm and h=3.5 mm on Ramp B/C only.

## 2) Accordion Profile (Alternative)

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

For Italian version, mirror labels in translated sheet variant.

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
- necromancer_dice_tower_sheet_01_body_a_v002.svg
- necromancer_dice_tower_sheet_02_body_b_v002.svg
- necromancer_dice_tower_sheet_03_ramps_v002.svg
- build_test_v002.md
