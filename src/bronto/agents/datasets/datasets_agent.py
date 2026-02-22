from ..base import BrontoAgent
from .dtos import DatasetsAgentSpec
from .enums import DatasetsAgentName


class DatasetsAgent(BrontoAgent):
    """Traceability agent for dataset discovery and key metadata tools."""

    def __init__(self):
        spec = DatasetsAgentSpec()
        super().__init__(
            name=DatasetsAgentName.DATASETS.value,
            description=spec.description,
            tools=spec.tools,
        )
