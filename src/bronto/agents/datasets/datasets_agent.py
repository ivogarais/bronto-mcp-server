from ..base import BrontoAgent
from .dtos import DatasetsAgentSpec
from .enums import DatasetsAgentName


class DatasetsAgent(BrontoAgent):
    """Agent for dataset discovery and metadata tools."""

    def __init__(self):
        """Initialize the datasets agent."""
        spec = DatasetsAgentSpec()
        super().__init__(
            name=DatasetsAgentName.DATASETS.value,
            description=spec.description,
            tools=spec.tools,
        )
