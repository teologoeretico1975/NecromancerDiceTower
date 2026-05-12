# Necromancer Dice Tower — Agent Instructions

You are working on a printable papercraft Etsy product.

Product:
Necromancer Dice Tower — Printable Papercraft PDF Kit

Project source of truth:
- `00_Project_Control/project_state.md`
- `01_Technical_Template/specs/technical_spec_v001.md`

Main task:
Generate and maintain real A4 SVG papercraft templates.

Working Language: Italian, English

Critical SVG rules:
- Use A4 page size.
- SVG must use `width="210mm"`, `height="297mm"`, `viewBox="0 0 210 297"`.
- Treat 1 SVG unit as 1 mm.
- Keep a 10 mm safe print margin.
- Every sheet must include a 20 × 20 mm scale check square.
- Use simple geometric SVG elements: rect, line, path, text, polygon.
- Do not use raster images in technical templates.
- Do not create decorative artwork in technical v001.
- The goal is physical build testing, not beauty.

Line style rules:
- Solid black line = cut.
- Dashed blue line = valley fold.
- Dotted red line = mountain fold.
- Light gray filled area = glue tab.

File rules:
- Save SVG sheets in `01_Technical_Template/svg/`.
- Save exported PDFs in `01_Technical_Template/pdf/`.
- Use versioned filenames ending in `_v001`, `_v002`, etc.
- Do not overwrite previous versions without explicit instruction.
- Keep SVG source editable and human-readable.

Product constraints:
- A4 paper.
- Print at 100%.
- Recommended cardstock: 200–250 gsm.
- No D&D references in product title or listing copy.
- Use “tabletop RPG”, “fantasy dice tower”, “printable papercraft”.
- Digital download only.
- No physical item will be shipped.
- No 3D printer required.
- No laser cutter required.

Quality rules:
- Do not generate vague mockups.
- Do not generate image-like SVG art for the technical phase.
- Use exact dimensions from the technical specification.
- Include labels on each piece.
- Include cut/fold/glue legend.
- Include comments in SVG explaining major sections.
