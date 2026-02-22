from .base import BrontoAgentRegistry
from .api_keys import ApiKeysAgent
from .context import ContextAgent
from .dashboard import DashboardAgent
from .datasets import DatasetsAgent
from .exports import ExportsAgent
from .forward import ForwardAgent
from .search import SearchAgent
from .statement_ids import StatementIdsAgent
from .usage import UsageAgent
from .users import UsersAgent


def build_agent_registry() -> BrontoAgentRegistry:
    return BrontoAgentRegistry(
        agents=[
            SearchAgent(),
            DatasetsAgent(),
            StatementIdsAgent(),
            DashboardAgent(),
            ApiKeysAgent(),
            UsersAgent(),
            ContextAgent(),
            ExportsAgent(),
            UsageAgent(),
            ForwardAgent(),
        ]
    )
