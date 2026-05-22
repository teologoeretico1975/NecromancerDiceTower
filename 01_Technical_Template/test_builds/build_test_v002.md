# Build Test v002

## Prototype

Necromancer Dice Tower - Technical Template v002 (Stepped/Accordion Ramps)

## Print Settings

- Paper size: A4
- Scale: 100%
- Fit to page: disabled
- Paper/cardstock used:
- Printer:
- Date: 2026-05-20

---

## Automated SVG Preflight (Agent 03)

Script used:

```text
01_Technical_Template/test_builds/agent_03_svg_build_test.py
```

Execution command:

```text
/workspaces/NecromancerDiceTower/.venv/bin/python 01_Technical_Template/test_builds/agent_03_svg_build_test.py
```

Execution result:

- sheet_01_body_a.svg: PASS
- sheet_02_body_b.svg: PASS
- sheet_03_ramps_ab.svg: PASS
- sheet_04_ramp_c.svg: PASS
- sheet_05_base_tray.svg: PASS
- OVERALL: PASS

Checks covered by Agent 03:

- A4 root size and viewBox (210mm x 297mm, 0 0 210 297)
- Legend and 20 x 20 mm scale text
- Line conventions present (black cut, blue dashed valley, red dotted mountain)
- Glue tab fill present (#e6e6e6)
- v002 anchors on Sheet 01/02 (A-L, A-R, B-L, B-R, C-L, C-R)
- v002 ramp labels on Sheet 03/04 (HIGH SIDE, LOW SIDE, GLUE TO WALL, FLOW ->)

Limitations:

- This preflight does not replace physical print/build/dice-roll tests.

---

## Print Test

- [ ] Printed at 100%
- [ ] Scale square correct: 20 x 20 mm
- [ ] Lines readable
- [ ] Margins ok
- [ ] No clipped elements

Notes:

---

## Cutting Test

- [ ] Tabs easy to cut
- [ ] Pieces not too small
- [ ] Exit opening manageable
- [ ] Ramp pieces manageable
- [ ] Labels clear

Notes:

---

## Folding Test

- [ ] Fold map understood (valley/mountain alternation)
- [ ] Ramp corrugation stays consistent
- [ ] Side walls hold shape
- [ ] Tabs align with walls

Notes:

---

## Assembly Test

- [ ] Body stable
- [ ] Anchor marks used on both walls
- [ ] HIGH SIDE and LOW SIDE orientation respected
- [ ] Landing zones preserved between ramps
- [ ] Base tray works
- [ ] Tower attaches to tray

Notes:

---

## Build Test Focus — Sheet 05 Terrace (2026-05-22)

Target geometry baseline (current technical set):
- Tower footprint: 65 x 65 mm
- Sheet 05 tray floor: 100 x 130 mm
- Effective visible terrace target: about 65 mm

Sheet 05 checks:
- [ ] F1/F2/F3/F4 fold cleanly to 90° without tearing
- [ ] F5(M) mountain fold is clear and stable after glue cure
- [ ] Rear flap (65 mm) aligns with tower coupling zone
- [ ] Front lip keeps dice in tray during normal d20 rolls
- [ ] No annotation overlap affects assembly readability

Terrace visibility and exit checks:
- [ ] At rest, exited die is visible from top-front user view
- [ ] Dice do not rebound out of tray in 20 test rolls (d6)
- [ ] Dice remain catchable without entering tower base area
- [ ] At least 80% of exits land in visible terrace zone

Record measured values:

| Metric | Target | Measured | Pass/Fail | Notes |
|---|---:|---:|---|---|
| Tower footprint width | 65 mm | | | |
| Rear flap width | 65 mm | | | |
| Tray floor depth | 130 mm | | | |
| Effective terrace depth | 65 mm | | | |
| Front lip height | 10 mm | | | |

---

## Ramp Geometry Verification

Record real build measurements:

| Ramp | Profile Type | Pitch p (mm) | Rise/Depth h (mm) | Modules | Side Wall (mm) | Clear Width (mm) |
|---|---|---:|---:|---:|---:|---:|
| A | | | | | | |
| B | | | | | | |
| C | | | | | | |

---

## Dice Flow Test (Quantitative)

Targets:
- d4 success >= 92%, jams <= 8%
- d6 success >= 96%, jams <= 4%
- d8/d10/d12/d20 success >= 95%, jams <= 5%

| Die | Rolls Tested | Successful Exits | Jams | Success % | Jam % | Avg Direction Changes | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| d4 | 50 | | | | | | |
| d6 | 50 | | | | | | |
| d8 | 30 | | | | | | |
| d10 | 30 | | | | | | |
| d12 | 30 | | | | | | |
| d20 | 30 | | | | | | |

---

## Jam Hotspot Tracking

Mark recurring jam points by location and frequency.

| Hotspot ID | Ramp/Area | Dice Type | Count | Trigger Condition | Proposed Fix |
|---|---|---|---:|---|---|
| H1 | | | | | |
| H2 | | | | | |
| H3 | | | | | |

---

## Structural Durability Check

Run cumulative stress test:
- Total rolls: 200 minimum

Checks:
- [ ] Ramp sag <= 3 mm at mid-span
- [ ] No delamination on tabs
- [ ] No wall detachment
- [ ] No geometry collapse after repeated use

Notes:

---

## Problems Found

1.
2.
3.

---

## Corrections Needed for v003

1.
2.
3.

---

## Decision

Ready for art pass:

```text
YES / NO
```

Reason:

---

## Pass Criteria (Go / No-Go)

Use this gate after completing all checks above.

Go to art pass only if all mandatory criteria pass:

1. Geometry and print fidelity
	- [ ] Scale square = 20 x 20 mm (tolerance +/- 0.5 mm)
	- [ ] Tower footprint measured = 65 x 65 mm (tolerance +/- 1 mm)
	- [ ] Tray floor measured = 100 x 130 mm (tolerance +/- 1 mm)
	- [ ] Rear flap width measured = 65 mm (tolerance +/- 1 mm)

2. Tray behavior (Sheet 05)
	- [ ] Effective visible terrace depth >= 60 mm
	- [ ] No dice rebound-out events in 20 d6 rolls
	- [ ] >= 80% of exits land in visible terrace zone

3. Dice flow reliability
	- [ ] d4 success >= 92% and jam <= 8%
	- [ ] d6 success >= 96% and jam <= 4%
	- [ ] d8/d10/d12/d20 success >= 95% and jam <= 5%

4. Structural integrity
	- [ ] Ramp sag <= 3 mm after 200 cumulative rolls
	- [ ] No tab delamination or wall detachment

Decision rule:
- If all mandatory criteria pass -> mark Decision = YES.
- If one or more mandatory criteria fail -> mark Decision = NO and log fixes in "Corrections Needed for v003".

---

## Photo Checklist

- [ ] Printed sheets before cutting
- [ ] Ramp fold map close-up
- [ ] Anchor alignment on both inner walls
- [ ] Ramp A/B/C installed
- [ ] Dice flow sequence (video or burst photos)
- [ ] Jam hotspot close-ups
- [ ] Finished prototype

---

## v003 Revision Summary

| Area | Problem | Proposed Fix | Severity |
|---|---|---|---|
| Body | | | |
| Ramps | | | |
| Exit | | | |
| Tray | | | |
| Instructions | | | |
| Other | | | |

Severity values:

```text
Critical / Important / Minor
```
