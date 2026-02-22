from ..base import BrontoAgent
from .dtos import ExportsAgentSpec
from .enums import ExportsAgentName


class ExportsAgent(BrontoAgent):
    """Traceability agent for export status tools."""

    def __init__(self):
        spec = ExportsAgentSpec()
        super().__init__(
            name=ExportsAgentName.EXPORTS.value,
            description=spec.description,
            tools=spec.tools,
        )
