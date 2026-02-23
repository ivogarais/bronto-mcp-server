from .base import BrontoAgentRegistry
from .access import AccessAgent
from .api_keys import ApiKeysAgent
from .context import ContextAgent
from .dashboard import DashboardAgent
from .dashboards_api import DashboardsApiAgent
from .datasets import DatasetsAgent
from .encryption_keys import EncryptionKeysAgent
from .exports import ExportsAgent
from .forward import ForwardAgent
from .groups import GroupsAgent
from .monitors import MonitorsAgent
from .parsers import ParsersAgent
from .policies import PoliciesAgent
from .search import SearchAgent
from .statement_ids import StatementIdsAgent
from .tags import TagsAgent
from .usage import UsageAgent
from .users import UsersAgent


def build_agent_registry() -> BrontoAgentRegistry:
    """Build the default MCP agent registry.

    Returns
    -------
    BrontoAgentRegistry
        Registry with all enabled agents.
    """
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
            GroupsAgent(),
            MonitorsAgent(),
            DashboardsApiAgent(),
            AccessAgent(),
            TagsAgent(),
            ParsersAgent(),
            PoliciesAgent(),
            EncryptionKeysAgent(),
        ]
    )
