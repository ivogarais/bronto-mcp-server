from ..base import BrontoAgent
from .dtos import ExportsAgentSpec
from .enums import ExportsAgentName


class ExportsAgent(BrontoAgent):
    """Agent for export lifecycle tools."""

    def __init__(self):
        """Initialize the exports agent."""
        spec = ExportsAgentSpec()
        super().__init__(
            name=ExportsAgentName.EXPORTS.value,
            description=spec.description,
            tools=spec.tools,
        )
