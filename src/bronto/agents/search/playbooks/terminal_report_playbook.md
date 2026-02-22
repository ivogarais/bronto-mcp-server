Terminal Report Playbook

Goal:
- Render readable reports for any terminal using plain ASCII only.
- Keep output deterministic, compact, and copy/paste friendly.

Hard formatting rules:
1) Do not use Markdown tables.
2) Do not use Unicode box-drawing characters.
3) Do not use ANSI colors, emojis, or visual widgets.
4) Use only plain text and ASCII borders: `+`, `-`, `|`.
5) Keep line width <= 100 characters when practical.
6) Wrap long cell values to the next line instead of letting borders break.

Recommended report structure:
1) Header lines
   - `<REPORT TITLE>`
   - `Window: <start> -> <end> (UTC)`
   - `Dataset: <name> (<log_id>)`
2) Summary section with a small ASCII table.
3) Detailed breakdown section with an ASCII table.
4) Optional `Exact Origin Code Lines` section with:
   - Statement ID
   - Source path and line number
   - Exact source code line
5) Closing line with next action or rerun hint.

ASCII table contract:
- Border row: `+-----+------+...+`
- Header row: `| Col | Col2 | ... |`
- Separator row under header.
- One row per record.
- Final bottom border.

If data is empty:
- Keep sections.
- Print `No rows` inside the relevant section instead of removing it.

Quality checks before sending:
- Borders align.
- No broken columns.
- No markdown table pipes without borders.
- No line exceeds readability limits due to unwrapped values.
