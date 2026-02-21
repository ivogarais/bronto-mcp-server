from .base import BrontoAgentRegistry
from .datasets_agent import DatasetsAgent
from .search_agent import SearchAgent
from .statement_ids_agent import StatementIdsAgent


def create_default_agent_registry() -> BrontoAgentRegistry:
    return BrontoAgentRegistry(
        agents=[
            SearchAgent(),
            DatasetsAgent(),
            StatementIdsAgent(),
        ]
    )
