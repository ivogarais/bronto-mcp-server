from .base import BrontoAgentRegistry
from .datasets import DatasetsAgent
from .search import SearchAgent
from .statement_ids import StatementIdsAgent


def create_default_agent_registry() -> BrontoAgentRegistry:
    return BrontoAgentRegistry(
        agents=[
            SearchAgent(),
            DatasetsAgent(),
            StatementIdsAgent(),
        ]
    )
