# Changelog

## 2026-05-20 (Session 2)

### Updated

- Dev container now includes Inkscape auto-install in `postCreateCommand` for persistent PDF export capability.
- VS Code tasks fully aligned to current sheet-based SVG workflow (`sheet_01..sheet_05`).
- PDF export task count increased from 4 to 5 sheets (added `sheet_05_base_tray`).

### Fixed

- Resolved JSON schema validation error in `.devcontainer/devcontainer.json` and `.vscode/settings.json` (invalid `workbench.editorAssociations` value).
- PDF viewer extension pinned via:
  - `tomoki1207.pdf` in devcontainer extensions list.
  - `.vscode/extensions.json` with workspace recommendations.
- This prevents viewer loss across reload/rebuild cycles.

### Generated

- PDF exports of all 5 current sheets (11.4–12 KB each) saved to `01_Technical_Template/pdf/`.

## 2026-05-20 (Session 1)

### Added

- Persistent SVG generator script with merged-spec support: [agent_02b_svg_generator.py](agent_02b_svg_generator.py).
- Persistent automated build preflight script: [01_Technical_Template/test_builds/agent_03_svg_build_test.py](01_Technical_Template/test_builds/agent_03_svg_build_test.py).
- Dev container configuration: [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json).

### Updated

- Sheet 3 validation and A4 fit math in [01_Technical_Template/specs/technical_spec_v001.md](01_Technical_Template/specs/technical_spec_v001.md).
- Build test report updated with automated preflight outcomes in [01_Technical_Template/test_builds/build_test_v002.md](01_Technical_Template/test_builds/build_test_v002.md).
- SVG generator now loads all `technical_spec_v*.md` files and applies latest ramp overrides.

### Generated

- New technical sheets produced by Agent 02b:
	- [01_Technical_Template/svg/sheet_01_body_a.svg](01_Technical_Template/svg/sheet_01_body_a.svg)
	- [01_Technical_Template/svg/sheet_02_body_b.svg](01_Technical_Template/svg/sheet_02_body_b.svg)
	- [01_Technical_Template/svg/sheet_03_ramps_ab.svg](01_Technical_Template/svg/sheet_03_ramps_ab.svg)
	- [01_Technical_Template/svg/sheet_04_ramp_c.svg](01_Technical_Template/svg/sheet_04_ramp_c.svg)
	- [01_Technical_Template/svg/sheet_05_base_tray.svg](01_Technical_Template/svg/sheet_05_base_tray.svg)

### Removed

- Legacy versioned SVG/PDF/PNG exports cleaned during workspace reset and replaced by new sheet-based outputs.

## 2026-05-12

### Added

- Workspace custom agent for technical SVG generation: [.github/agents/technical-svg-template.agent.md](.github/agents/technical-svg-template.agent.md).
- Ramp-focused v002 specification addendum: [01_Technical_Template/specs/technical_spec_v002_ramps.md](01_Technical_Template/specs/technical_spec_v002_ramps.md).
- New technical build test checklist with quantitative flow metrics: [01_Technical_Template/test_builds/build_test_v002.md](01_Technical_Template/test_builds/build_test_v002.md).

### Created

- v002 SVG sheets:
	- [01_Technical_Template/svg/necromancer_dice_tower_sheet_01_body_a_v002.svg](01_Technical_Template/svg/necromancer_dice_tower_sheet_01_body_a_v002.svg)
	- [01_Technical_Template/svg/necromancer_dice_tower_sheet_02_body_b_v002.svg](01_Technical_Template/svg/necromancer_dice_tower_sheet_02_body_b_v002.svg)
	- [01_Technical_Template/svg/necromancer_dice_tower_sheet_03_ramps_v002.svg](01_Technical_Template/svg/necromancer_dice_tower_sheet_03_ramps_v002.svg)
- v002b readability-tuned SVG sheets:
	- [01_Technical_Template/svg/necromancer_dice_tower_sheet_01_body_a_v002b.svg](01_Technical_Template/svg/necromancer_dice_tower_sheet_01_body_a_v002b.svg)
	- [01_Technical_Template/svg/necromancer_dice_tower_sheet_02_body_b_v002b.svg](01_Technical_Template/svg/necromancer_dice_tower_sheet_02_body_b_v002b.svg)
	- [01_Technical_Template/svg/necromancer_dice_tower_sheet_03_ramps_v002b.svg](01_Technical_Template/svg/necromancer_dice_tower_sheet_03_ramps_v002b.svg)

### Updated

- Sheet 03 v002 explanatory text wrapped and moved to avoid truncation/overlap.
- White page background added to v002 sheets to improve preview readability on dark UI themes.
- PNG/PDF exports regenerated for v002 and v002b under [01_Technical_Template/pdf](01_Technical_Template/pdf) and [01_Technical_Template/exports_png](01_Technical_Template/exports_png).
