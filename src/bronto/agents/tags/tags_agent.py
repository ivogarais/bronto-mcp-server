from ..base import BrontoAgent
from .dtos import TagsAgentSpec
from .enums import TagsAgentName


class TagsAgent(BrontoAgent):
    """Agent for tag management tools."""

    def __init__(self):
        """Initialize the tags agent."""
        spec = TagsAgentSpec()
        super().__init__(
            name=TagsAgentName.TAGS.value,
            description=spec.description,
            tools=spec.tools,
        )
