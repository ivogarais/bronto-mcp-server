from enum import Enum


class TerminalReportsAgentName(str, Enum):
    TERMINAL_REPORTS = "terminal_reports"


class TerminalReportsToolName(str, Enum):
    RENDER_ASCII_TABLE = "render_ascii_table"
    VALIDATE_TERMINAL_REPORT = "validate_terminal_report"
    TERMINAL_REPORT_PLAYBOOK = "terminal_report_playbook"
