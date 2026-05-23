# Necromancer Dice Tower - Technical Specification v003 (Ramp Scale-Up + Notch Relief)

**Last Updated:** 2026-05-23
**Status:** Active – Addresses prototype feedback: ramps too small for 200–300 gsm cardstock

## Purpose

This addendum overrides v002 ramp geometry values with enlarged parameters that are
**manageable to fold with 200–300 gsm cardstock**.

Also mandates:
1. **45° relief notch cuts** at every step fold junction on side-wall strips
2. **Dedicated instruction sheet** (Sheet 06) for all fold/assembly guidance, freeing Sheets 03/04 for large clean ramp nets only

This file does not replace v001 or v002 entirely. It overrides only the ramp size parameters
and adds two mandatory construction features.

---

## Why the Original Ramps Were Too Small

v002 ramp values were:
- Tread p = 8 mm → folds require precise creasing in < 8 mm pitch
- Rise h = 3 mm → fold angle is steep and difficult with thick stock
- Modules = 8 → 8 folds per ramp, very laborious and error-prone

For 200–300 gsm cardstock, a **minimum tread of 12–15 mm** and a **minimum rise of 4–5 mm** are needed
to allow clean, accurate folding without paper tearing or deformation.

---

## New (v003) Ramp Geometry

### Stepped Profile (Default)

| Parameter | v002 Value | **v003 Value** | Notes |
|---|---:|---:|---|
| Ramp clear width | 57 mm | **65 mm** | Match tower shaft interior |
| Ramp effective run length | 70–81 mm | **84 mm** | 6 modules × 14 mm tread |
| Tread p | **8 mm** | **14 mm** | +75%; easier fold on thick card |
| Rise h | **3.0 mm** | **5.0 mm** | Deeper steps, more tactile fold |
| Number of modules per ramp | **8** | **6** | Fewer folds; same overall drop |
| Side tabs | 10 mm | **10 mm** | Unchanged |
| Back tab | 10 mm | **10 mm** | Unchanged |
| Side wall height on ramp | 5 mm | **5 mm** | Unchanged; clear path = 65–10 = 55 mm |

**Total cut dimensions per ramp:**
- Width: 10 (tab) + 65 (body) + 10 (tab) = **85 mm**
- Height including back tab: 10 + 84 = **94 mm**

Two ramps fit side-by-side on A4: 85 + 8 (gap) + 85 = 178 mm < 190 mm usable ✓

**Equivalent slope angle:** tan(θ) = 5/14 → θ ≈ 19.6° (same ballpark as v002)

### Total drop per ramp (6 modules × 5 mm rise = 30 mm)
Three ramps total: 3 × 30 mm = 90 mm vertical drop. Tower shaft height = 190 mm. Remaining 100 mm is used for entry, exit landing zones, and ramp mounting clearances.

---

## 45° Relief Notch Cuts (NEW – Mandatory)

### Problem

When the stepped ramp surface folds alternating valley/mountain, the side-wall strips
must bend 90° at each step junction. Without a notch, excess paper bunches at the inner
corner and prevents the fold from lying flat.

### Solution

At **every horizontal fold line** (each of the 5 internal fold lines per ramp, spaced every 14 mm),
within the **side-wall zones** (the inner 5 mm strips on left and right of the ramp body),
remove a right-angle triangle with legs equal to the rise `h = 5 mm`.

### Notch Geometry

```
Side wall strip cross-section at a fold line:

    ←  wall_h (5mm)  →
    ┌────────────────┐   ← fold line (step_y)
    │   NOTCH: cut   │
    │ ◣ (triangle)   │
    └────────────────┘
         ↑
    inner edge (tab side)   outer edge (ramp surface)
```

For each internal fold at position `step_y = y0 + i * tread` (i = 1..modules-1):

- **Left notch:** triangle with vertices:
  - `(x0 + tab_side,          step_y)`
  - `(x0 + tab_side + rise,   step_y)`
  - `(x0 + tab_side,          step_y + rise)`  ← points downward (toward low side)

- **Right notch:** triangle with vertices:
  - `(x0 + tab_side + body_w - rise,   step_y)`
  - `(x0 + tab_side + body_w,          step_y)`
  - `(x0 + tab_side + body_w,          step_y + rise)` ← points downward (mirrored)

Fill notch triangles with a **distinct color**: orange-red `#FF6600` with label "NOTCH: CUT & REMOVE".
Add a legend entry for this new symbol.

**Why pointing downward only?** The fold direction at each step causes the lower-side material
to collide. Alternating the notch direction (up/down) per fold would be more accurate but is
harder to follow for a first-time builder; therefore all notches point toward the low (exit) side
for consistency, and builders should follow the printed notch marks exactly.

---

## Dedicated Instruction Sheet (NEW – Sheet 06)

With instructions moved to Sheet 06, Sheets 03 and 04 contain ONLY:
- The ramp net(s) at full printable size
- Minimal necessary labels (RAMP A, HIGH SIDE, LOW SIDE, FLOW ->, fold IDs)
- The standard legend and scale square

Sheet 06 content:
1. **1-2-3 Fold Sequence** diagram (enlarged, clear stages: FLAT → SCORE & FOLD → GLUE)
2. **Notch explanation** with diagram and photo-quality cross-section sketch
3. **Assembly sequence overview** for all 3 ramps
4. **Material and tool tips** (scoring tool, bone folder, glue type)
5. **Verification checklist** (does the ramp lay flat? do side walls stand 90°?)

---

## Sheet Layout Changes (v003)

| Sheet | v002 Content | **v003 Content** |
|---|---|---|
| Sheet 03 | Ramp A + B side-by-side (cramped) | **RAMP A + RAMP B side-by-side (large, 85 mm each)** |
| Sheet 04 | Ramp C only | **RAMP C only (centered, large)** |
| Sheet 05 | Base tray | Base tray (unchanged) |
| **Sheet 06** | *(new)* | **Full instruction/fold-guide page** |

Note: Beginner-mode fold diagram on Sheet 03 is removed; all guidance centralised on Sheet 06.

---

## Clearance Constraints (Updated)

| Parameter | v002 | v003 |
|---|---:|---:|
| Minimum clear die path | 54 mm | 55 mm ✓ (65 − 2×5) |
| Side wall height | 4–6 mm | 5 mm |
| Landing zone between ramps | 8–12 mm | 10 mm (fits within transition) |

---

## Layout Lock Constraints (from Manual Readability Iteration)

The following are **mandatory generation constraints** derived from manually improved SVGs.
They are not optional cosmetic edits: they must be preserved by the regeneration algorithm.

### Sheet 01 / Sheet 02 (Body Panels)

1. Fold IDs near top edges (`F1`, `F2`) must be **vertical** (`rotate(-90)`) to keep the top instruction band clear.
2. Anchor labels (`A-L`, `A-R`, `B-L`, `B-R`, `C-L`, `C-R`) must be rendered as **vertical side labels**:
  - left side labels: `rotate(-90)`
  - right side labels: `rotate(90)`
3. `FOLD GUIDE` must be generated as a **multiline block** (title + 3 lines), not a single long line.

### Sheet 03 (Ramps A/B)

1. Use a **staggered layout** to avoid callout collisions:
  - Ramp A in upper-left zone
  - Ramp B in lower-right zone
2. Keep per-ramp explanatory callouts (`OUTER BLUE...`, `INNER BLUE...`, `ORANGE triangles...`) at reduced visual scale (about 80%) to preserve bottom legend clearance.

### Sheet 04 (Ramp C)

1. Ramp C text+net block must be placed lower than top header zone (manual profile), keeping clear white space under title/subtitle.
2. Explanatory callouts under ramp must use reduced scale (about 80%) to avoid overlap with legend.

### Sheet 05 (Base Tray)

1. Tray geometry/text cluster uses a shifted placement profile (manual readability offset), preserving an uncluttered top text band.
2. Micro-labels (`L - FRONT LIP`, `GLUE FLAP ...`) use smaller font (~2.88 px) to prevent spillover.

### Sheet 06 (Instructions)

1. Long explanatory text must use **algorithmic wrapping** (line splitting by max characters) for stable readability.
2. Section C and D lines must be wrapped and bounded to avoid collisions with legend and scale square.
3. Horizontal separators between sections are part of the required readability layout.

---

## Machine-Readable Override Values (parser target)

The following table uses exact format expected by the SVG generator.
These values override v001/v002 equivalents.

| Parameter | Value |
|---|---:|
| Ramp width | 65 mm |
| Ramp length | 84 mm |
| Tread p | 14 mm |
| Rise h | 5.0 mm |
| Number of modules per ramp | 6 |
| Side tabs | 10 mm |
| Back tab | 10 mm |
| Side wall height on ramp | 5 mm |

---

## Document History

- **v003.0 (2026-05-23):** Enlarged ramp geometry, added mandatory 45° notch cuts, moved all assembly instructions to Sheet 06.
- **v003.1 (2026-05-23):** Added locked text/layout constraints from manual readability edits (rotations, multiline blocks, wrapped text, staggered ramp text placement).
