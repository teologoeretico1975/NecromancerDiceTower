# Necromancer Dice Tower - Technical Specification v004 (Baffle Core Anti-Jam)

**Last Updated:** 2026-05-23  
**Status:** Active – Replaces ramp-based randomization with baffle structures after physical prototype feedback.

## Purpose

This addendum replaces the internal **RAMP A/B/C** concept with a **Baffle Core** system to improve die clearance and reduce jams on 200–250 gsm cardstock builds.

v004 keeps tower body/tray geometry from previous technical versions, but overrides the internal randomization architecture and assembly flow.

---

## Root Cause from Prototype

Observed issue: stepped ramps reduced effective free channel and created frequent blockage points.

Design response in v004:
- remove continuous internal ramps,
- use alternating bulkhead windows + staggered deflector fins,
- preserve a central free path for reliable die travel.

---

## v004 Internal Architecture (Mandatory)

### 1) Bulkheads (Sheet 03)

Two internal bulkheads are required:
- **B1** and **B2**
- body width: **55 mm**
- body height: **120 mm**
- side glue tabs: **5 mm** each side (total width 65 mm)

Window pattern:
- each bulkhead has 2 windows (**22 × 16 mm**)
- windows must alternate left/right
- B1 and B2 must be mirrored to create a chicane path

### 2) Deflector Fins (Sheet 04)

Six fins are required:
- **D1..D6**
- folded toward the center channel at **30–45°**
- installed staggered between left and right walls

Placement baseline:
- left wall: D1, D3, D5
- right wall: D2, D4, D6

### 3) Central Clearance (Critical)

During assembly and QA, enforce:
- **minimum free center channel >= 30 mm** along the full fall path.

If local channel width drops below 30 mm, rebuild alignment before closing the body seam.

---

## Assembly Overrides vs v003

1. Build body panels and tray as in current technical sheets.
2. Install **B1** in upper internal zone.
3. Install **B2** below B1 with **25–30 mm** vertical gap.
4. Install **D1..D6** staggered on side walls.
5. Verify center channel >= 30 mm.
6. Close body seam, attach tray, run drop tests.

RAMP A/B/C steps are deprecated in v004.

---

## Validation Targets (Physical)

Minimum pass thresholds:
- **d6 exit success >= 95%**
- **d20 exit success >= 90%**
- no persistent repeatable jam point at same location

If test fails:
1. reduce fin fold angle,
2. increase local channel width,
3. re-test.

---

## Technical Drawing Rules (Inherited)

- A4 SVG only: `width="210mm"`, `height="297mm"`, `viewBox="0 0 210 297"`
- 1 unit = 1 mm
- 10 mm safe margin
- 20 × 20 mm scale check square on every sheet
- legend on each sheet:
  - cut = solid black
  - valley fold = dashed blue
  - mountain fold = dotted red
  - glue tab = light gray fill

---

## File Mapping (v004)

- Sheet 03 (`sheet_03_ramps_ab.svg`): repurposed as **Baffle Core Bulkheads** (B1/B2)
- Sheet 04 (`sheet_04_ramp_c.svg`): repurposed as **Baffle Core Deflectors** (D1..D6)
- Sheet 06 (`sheet_06_instructions.svg`): updated assembly instructions for baffle workflow

Existing filenames are preserved for pipeline compatibility.

---

## Document History

- **v004.0 (2026-05-23):** Introduced Baffle Core anti-jam architecture; ramp system deprecated for technical prototype line.
