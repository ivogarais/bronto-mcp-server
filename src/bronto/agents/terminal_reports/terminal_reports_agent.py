from ..base import BrontoAgent
from .dtos import TerminalReportsAgentSpec
from .enums import TerminalReportsAgentName


class TerminalReportsAgent(BrontoAgent):
    """Agent focused on deterministic terminal report formatting."""

    def __init__(self):
        spec = TerminalReportsAgentSpec()
        super().__init__(
            name=TerminalReportsAgentName.TERMINAL_REPORTS.value,
            description=spec.description,
            tools=spec.tools,
        )
