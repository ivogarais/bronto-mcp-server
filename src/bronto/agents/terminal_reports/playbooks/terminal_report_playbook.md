Terminal Report Playbook

Goal:
- Produce terminal-safe reports with deterministic ASCII formatting.
- Ensure output passes formatting validation before sending to the user.

Required flow:
1) Build structured rows and columns from computed data.
2) Call `render_ascii_table` to produce the table text.
3) Build final report text around rendered sections.
4) Call `validate_terminal_report` on the full report text.
5) If `valid=false`, fix violations and validate again before responding.

Hard constraints:
- Use plain ASCII only.
- Do not use markdown tables.
- Do not use Unicode box drawing characters.
- Do not use ANSI color escape sequences.
- Keep lines within configured max width.

Recommended sections:
- Header: title, window, dataset.
- Summary table.
- Detailed breakdown table.
- Optional exact origin code lines table.
- Next action line.
