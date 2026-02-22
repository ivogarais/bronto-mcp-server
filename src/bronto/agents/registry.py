from .base import BrontoAgentRegistry
from .dashboard import DashboardAgent
from .datasets import DatasetsAgent
from .search import SearchAgent
from .statement_ids import StatementIdsAgent


def build_agent_registry() -> BrontoAgentRegistry:
    return BrontoAgentRegistry(
        agents=[
            SearchAgent(),
            DatasetsAgent(),
            StatementIdsAgent(),
            DashboardAgent(),
        ]
    )
