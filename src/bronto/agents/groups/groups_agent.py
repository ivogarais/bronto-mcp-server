from ..base import BrontoAgent
from .dtos import GroupsAgentSpec
from .enums import GroupsAgentName


class GroupsAgent(BrontoAgent):
    """Agent for group and membership tools."""

    def __init__(self):
        """Initialize the groups agent."""
        spec = GroupsAgentSpec()
        super().__init__(
            name=GroupsAgentName.GROUPS.value,
            description=spec.description,
            tools=spec.tools,
        )
