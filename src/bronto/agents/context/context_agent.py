from ..base import BrontoAgent
from .dtos import ContextAgentSpec
from .enums import ContextAgentName


class ContextAgent(BrontoAgent):
    """Traceability agent for context retrieval tools."""

    def __init__(self):
        spec = ContextAgentSpec()
        super().__init__(
            name=ContextAgentName.CONTEXT.value,
            description=spec.description,
            tools=spec.tools,
        )
