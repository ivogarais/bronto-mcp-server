from ..base import BrontoAgent
from .dtos import UsersAgentSpec
from .enums import UsersAgentName


class UsersAgent(BrontoAgent):
    """Traceability agent for user directory discovery tools."""

    def __init__(self):
        spec = UsersAgentSpec()
        super().__init__(
            name=UsersAgentName.USERS.value,
            description=spec.description,
            tools=spec.tools,
        )
