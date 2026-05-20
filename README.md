# Necromancer Dice Tower

A themed dice tower project with tracked specs, controlled execution phases, and automation-first validation.

## v002 Progress Update
- Specification stream has been merged into the active generation workflow.
- Automated preflight has been added to verify environment readiness before execution.
- Devcontainer/tooling updated for repeatable Python 3.11 setup with Inkscape and PDF export automation.
- PDF export tasks (`.vscode/tasks.json`) fully aligned to current sheet-based workflow.
- PDF viewer extension (`tomoki1207.pdf`) pinned in devcontainer and workspace recommendations for stable UX after reload/rebuild.

## Current Focus
- Stabilize the v002 pipeline with persistent tooling and keep docs synchronized with execution state.
- Ensure repeatable export workflow (SVG → PDF) survives devcontainer rebuilds.

## Next Steps
1. Execute the **physical build test** for the current tower configuration (`sheet_01..sheet_05` PDFs).
2. Capture test observations (alignment, feed reliability, structural stability).
3. Record dice-flow metrics and jam hotspots in `build_test_v002.md`.
4. Feed findings back into the next specification and iteration pass.
