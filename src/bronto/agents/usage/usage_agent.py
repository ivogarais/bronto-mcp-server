from ..base import BrontoAgent
from .dtos import UsageAgentSpec
from .enums import UsageAgentName


class UsageAgent(BrontoAgent):
    """Traceability agent for usage analytics tools."""

    def __init__(self):
        spec = UsageAgentSpec()
        super().__init__(
            name=UsageAgentName.USAGE.value,
            description=spec.description,
            tools=spec.tools,
        )
