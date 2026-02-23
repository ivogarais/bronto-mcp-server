from ..base import BrontoAgent
from .dtos import UsersAgentSpec
from .enums import UsersAgentName


class UsersAgent(BrontoAgent):
    """Agent for user lifecycle tools."""

    def __init__(self):
        """Initialize the users agent."""
        spec = UsersAgentSpec()
        super().__init__(
            name=UsersAgentName.USERS.value,
            description=spec.description,
            tools=spec.tools,
        )
