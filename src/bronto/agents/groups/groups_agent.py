from ..base import BrontoAgent
from .dtos import GroupsAgentSpec
from .enums import GroupsAgentName


class GroupsAgent(BrontoAgent):
    def __init__(self):
        spec = GroupsAgentSpec()
        super().__init__(name=GroupsAgentName.GROUPS.value, description=spec.description, tools=spec.tools)
