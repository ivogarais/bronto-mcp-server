from ..base import BrontoAgent
from .dtos import TagsAgentSpec
from .enums import TagsAgentName


class TagsAgent(BrontoAgent):
    def __init__(self):
        spec = TagsAgentSpec()
        super().__init__(name=TagsAgentName.TAGS.value, description=spec.description, tools=spec.tools)
