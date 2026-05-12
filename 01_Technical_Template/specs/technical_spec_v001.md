# Necromancer Dice Tower — Technical Specification v001

## Purpose

This document defines the first technical prototype for a printable A4 papercraft dice tower.

This is not the final decorated product.  
The purpose of v001 is to verify that the tower can be printed, cut, folded, glued, and used with standard tabletop RPG dice.

---

## Product Type

Printable papercraft dice tower.

## Format

- Paper size: A4
- Print scale: 100%
- Recommended material: 200–250 gsm cardstock
- Tools: scissors or craft knife, ruler, glue stick or PVA glue
- Skill level: beginner/intermediate papercraft

---

## Target Dice Compatibility

The tower should work with a standard tabletop RPG dice set:

- d4
- d6
- d8
- d10
- d12
- d20

The d20 is the main reference die for internal clearance.

---

## Overall Tower Dimensions

Proposed external dimensions:

| Dimension | Value |
|---|---:|
| Height | 190 mm |
| Width | 65 mm |
| Depth | 65 mm |

Proposed internal space:

| Dimension | Value |
|---|---:|
| Internal width | approx. 58–60 mm |
| Internal depth | approx. 58–60 mm |

Reasoning:

- Wide enough for standard dice.
- Still compact enough for A4 papercraft.
- Tall enough for 3 internal ramps.
- Not too large for a first product.

---

## Main Components

The prototype should include:

1. Main tower body
2. Internal ramp A
3. Internal ramp B
4. Internal ramp C
5. Top opening reinforcement
6. Front exit arch or rectangular exit
7. Optional base tray
8. Glue tabs
9. Scale check square
10. Cut/fold/glue legend

---

## A4 Sheet Plan

### Sheet 1 — Main Tower Body

Contains:

- front panel
- left side panel
- right side panel
- back panel
- vertical glue tab
- bottom tabs if needed
- front dice exit cutout
- top dice opening

Approximate panel dimensions:

| Part | Width | Height |
|---|---:|---:|
| Front panel | 65 mm | 190 mm |
| Left side panel | 65 mm | 190 mm |
| Back panel | 65 mm | 190 mm |
| Right side panel | 65 mm | 190 mm |
| Side glue tab | 10–12 mm | 190 mm |

Total flat width:

```text
65 + 65 + 65 + 65 + 12 = 272 mm
```

This does not fit on A4 portrait width.

Therefore the body cannot be a single horizontal strip on one A4 portrait page.

### Required Solution

Split the body into two pieces:

#### Body Part A

- front panel
- left side panel
- glue tab

#### Body Part B

- back panel
- right side panel
- glue tabs

This allows the tower body to fit on A4 pages.

---

## Sheet 1 — Body Part A

Suggested parts:

| Part | Size |
|---|---:|
| Front panel | 65 × 190 mm |
| Left side panel | 65 × 190 mm |
| Glue tab | 10 × 190 mm |

Approximate flat width:

```text
65 + 65 + 10 = 140 mm
```

This fits on A4.

Include:

- front exit cutout
- fold line between front and left side
- glue tab on one side
- labels: FRONT, LEFT SIDE, GLUE TAB
- scale check square 20 × 20 mm

---

## Sheet 2 — Body Part B

Suggested parts:

| Part | Size |
|---|---:|
| Back panel | 65 × 190 mm |
| Right side panel | 65 × 190 mm |
| Glue tab A | 10 × 190 mm |
| Glue tab B | 10 × 190 mm |

Approximate flat width:

```text
10 + 65 + 65 + 10 = 150 mm
```

This fits on A4.

Include:

- fold line between back and right side
- glue tabs
- labels: BACK, RIGHT SIDE, GLUE TAB

---

## Sheet 3 — Internal Ramps

The tower should use 3 internal ramps.

### Ramp Dimensions

Suggested ramp body:

| Dimension | Value |
|---|---:|
| Ramp width | 58 mm |
| Ramp length | 70 mm |
| Side glue tabs | 8–10 mm each |
| Back glue tab | 8–10 mm |

The ramps should be slightly narrower than the internal width.

If the internal width is approx. 60 mm, use:

```text
Ramp width: 56–58 mm
```

### Ramp Angle

Target ramp angle:

```text
35°–45°
```

For v001, use a practical fold-and-glue ramp rather than a mathematically perfect one.

### Ramp Placement

Suggested placement from top:

| Ramp | Approx. Height from Bottom | Direction |
|---|---:|---|
| Ramp A | 145 mm | slopes down left-to-right |
| Ramp B | 95 mm | slopes down right-to-left |
| Ramp C | 45 mm | slopes down left-to-right toward exit |

This creates a zig-zag dice path.

---

## Sheet 4 — Base Tray / Exit Tray

Optional for v001 but recommended for sellable product.

Suggested tray dimensions:

| Part | Size |
|---|---:|
| Tray floor | 95 × 90 mm |
| Front wall | 95 × 25 mm |
| Left wall | 90 × 25 mm |
| Right wall | 90 × 25 mm |
| Back connection flap | 65 × 20 mm |

The tray catches dice after they exit the tower.

For v001, the tray can be simple and rectangular.

---

## Dice Exit

Minimum suggested opening:

| Dimension | Value |
|---|---:|
| Width | 45–50 mm |
| Height | 38–45 mm |

Recommended v001:

```text
50 mm wide × 42 mm high
```

Shape:

- rectangular for technical v001
- gothic arch for final art version

The technical prototype may use a rectangular exit to simplify cutting.

---

## Top Opening

Suggested opening:

```text
50 mm × 50 mm minimum
```

The top can remain open in v001.

Optional later:

- decorative top rim
- gothic crenellations
- skull ornament
- rune border

---

## Glue Tab Strategy

Recommended glue tab width:

```text
8–12 mm
```

Rules:

- Use 10 mm tabs for main body joins.
- Use 8 mm tabs for ramps.
- Use 10 mm tabs for tray walls.
- Avoid very small tabs below 6 mm.
- Mark all glue tabs clearly with light gray fill and “GLUE”.

---

## Line Legend

Use this convention in SVG/PDF:

| Line Type | Meaning |
|---|---|
| Solid black line | Cut |
| Dashed blue line | Valley fold |
| Dotted red line | Mountain fold |
| Light gray area | Glue tab |
| Numbered circle | Assembly order |

---

## Scale Check

Every printable sheet should include:

```text
20 mm × 20 mm scale check square
```

Label:

```text
Scale check: this square must measure 20 × 20 mm when printed at 100%.
```

---

## Assembly Order

Recommended v001 assembly:

1. Print all sheets at 100%.
2. Check the 20 × 20 mm scale square.
3. Cut Body Part A.
4. Cut Body Part B.
5. Score fold lines.
6. Pre-fold body panels.
7. Cut front dice exit.
8. Glue Body Part A and Body Part B together.
9. Glue the tower body into a rectangular tube.
10. Cut and fold Ramp A.
11. Insert and glue Ramp A.
12. Cut and fold Ramp B.
13. Insert and glue Ramp B.
14. Cut and fold Ramp C.
15. Insert and glue Ramp C.
16. Assemble optional base tray.
17. Attach tower to base tray.
18. Let glue dry fully.
19. Test dice flow.

---

## Physical Build Test

### Print Test

- [ ] Printed on A4
- [ ] Printed at 100%
- [ ] “Fit to page” disabled
- [ ] Scale square measures 20 × 20 mm
- [ ] Lines are readable
- [ ] No important elements clipped by printer margins

### Cutting Test

- [ ] Cut lines are clear
- [ ] Exit opening is easy enough to cut
- [ ] Tabs are not too small
- [ ] Ramps are not too fiddly
- [ ] Pieces are labeled clearly

### Folding Test

- [ ] Fold lines are understandable
- [ ] Body closes into a rectangle
- [ ] Glue tabs align
- [ ] Ramps can be folded cleanly

### Assembly Test

- [ ] Body stands upright
- [ ] Ramps are reachable during assembly
- [ ] Ramps can be glued without excessive frustration
- [ ] Tray connects correctly
- [ ] Model feels stable enough

### Dice Test

- [ ] d20 enters from top
- [ ] d20 does not jam frequently
- [ ] dice bounce across ramps
- [ ] dice exit from front
- [ ] tray catches dice
- [ ] tower does not tip over during normal use

---

## Common Failure Points

### Failure 1 — Body strip too wide for A4

Mitigation:

- split tower body into two printable pieces.

### Failure 2 — Ramps difficult to glue inside tower

Mitigation:

- add large side tabs.
- mark ramp positions inside panels before closing tower body.
- consider gluing ramps before fully closing the body.

### Failure 3 — Dice jam inside tower

Mitigation:

- increase internal width.
- reduce ramp length.
- increase vertical spacing.
- use smoother ramp angles.

### Failure 4 — Exit too small

Mitigation:

- enlarge exit to at least 50 × 42 mm.
- avoid decorative details that reduce clearance.

### Failure 5 — Tower tips over

Mitigation:

- add base tray.
- slightly widen tray.
- keep tower height below 220 mm.

---

## Acceptance Criteria for Technical v001

The technical prototype passes if:

- [ ] All parts fit on A4 pages.
- [ ] Template prints at 100%.
- [ ] Scale square is correct.
- [ ] Tower can be assembled by one person.
- [ ] The body closes correctly.
- [ ] At least 80% of dice test rolls exit successfully.
- [ ] The model stands upright.
- [ ] No critical part requires impossible gluing.
- [ ] Required corrections are manageable in v002.

---

## Notes for Later Art Pass

Do not add final artwork until the physical prototype passes.

Future decorative surfaces:

- front panel: gothic arch, skull emblem, rune border
- side panels: cracked stone texture
- back panel: larger rune pattern
- top rim: necromantic glow
- exit area: gothic gate shape
- tray floor: ritual circle or cracked stone floor

Final variants:

- full color
- low ink
- black and white coloring version
