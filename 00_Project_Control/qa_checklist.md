# QA Checklist — Technical Template Gate (v002)

## Scope

Use this checklist as the project-level gate before moving from technical template to art pass.
Reference measurements and roll outcomes from:
- [01_Technical_Template/test_builds/build_test_v002.md](01_Technical_Template/test_builds/build_test_v002.md)

---

## 1) Print and Scale Fidelity (Mandatory)

- [ ] Printed on A4 at 100% scale (Fit to page disabled)
- [ ] 20 x 20 mm scale square measured within +/- 0.5 mm
- [ ] No clipped geometry and margins are safe (>= 10 mm)

---

## 2) Dimensional Conformance (Mandatory)

- [ ] Tower footprint measured = 65 x 65 mm (+/- 1 mm)
- [ ] Tray floor measured = 100 x 130 mm (+/- 1 mm)
- [ ] Rear flap width measured = 65 mm (+/- 1 mm)
- [ ] Effective visible terrace depth >= 60 mm

---

## 3) Assembly Readability and Fit (Mandatory)

- [ ] Fold IDs are clear and non-overlapping (including F5(M) on Sheet 05)
- [ ] F1/F2/F3/F4 fold cleanly to 90°
- [ ] F5(M) mountain fold remains stable after glue cure
- [ ] Tray tabs and side walls align without forced deformation

---

## 4) Dice Exit and Catch Behavior (Mandatory)

- [ ] No dice rebound-out events in 20 d6 test rolls
- [ ] >= 80% of exits land in visible terrace zone
- [ ] Exited die remains visible from normal top-front user view

---

## 5) Dice Flow Reliability (Mandatory)

- [ ] d4 success >= 92% and jam <= 8%
- [ ] d6 success >= 96% and jam <= 4%
- [ ] d8/d10/d12/d20 success >= 95% and jam <= 5%

---

## 6) Structural Durability (Mandatory)

- [ ] Ramp sag <= 3 mm after 200 cumulative rolls
- [ ] No tab delamination
- [ ] No wall detachment
- [ ] No geometry collapse after repeated use

---

## Go / No-Go Rule

- **GO (Art Pass):** all mandatory checks above pass.
- **NO-GO:** one or more mandatory checks fail; record fixes in build test under "Corrections Needed for v003".

Decision:
- [ ] GO
- [ ] NO-GO

Date:
Tester:
Notes:

