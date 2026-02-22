from bronto.agents.access import AccessAgent
from bronto.agents.api_keys import ApiKeysAgent
from bronto.agents.context import ContextAgent
from bronto.agents.dashboard import DashboardAgent
from bronto.agents.dashboards_api import DashboardsApiAgent
from bronto.agents.datasets import DatasetsAgent
from bronto.agents.encryption_keys import EncryptionKeysAgent
from bronto.agents.exports import ExportsAgent
from bronto.agents.forward import ForwardAgent
from bronto.agents.groups import GroupsAgent
from bronto.agents.monitors import MonitorsAgent
from bronto.agents.parsers import ParsersAgent
from bronto.agents.policies import PoliciesAgent
from bronto.agents.search import SearchAgent
from bronto.agents.statement_ids import StatementIdsAgent
from bronto.agents.tags import TagsAgent
from bronto.agents.usage import UsageAgent
from bronto.agents.users import UsersAgent


def test_datasets_agent_contract():
    agent = DatasetsAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "datasets"
    assert "Discovers datasets" in agent.description
    assert tool_names == {
        "get_datasets",
        "create_log",
        "get_datasets_by_name",
        "get_keys",
        "get_all_datasets_keys",
        "get_key_values",
        "datasets_playbook",
    }


def test_search_agent_contract():
    agent = SearchAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "search"
    assert "Searches Bronto log events" in agent.description
    assert tool_names == {
        "search_logs",
        "get_search_status",
        "cancel_search",
        "compute_metrics",
        "get_timestamp_as_unix_epoch",
        "get_current_time",
        "search_logs_playbook",
        "compute_metrics_playbook",
    }


def test_statement_ids_agent_contract():
    agent = StatementIdsAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "statement_ids"
    assert "statement IDs" in agent.description
    assert tool_names == {
        "create_stmt_id",
        "deploy_statements",
        "statement_ids_playbook",
        "inject_stmt_ids",
        "extract_stmt_ids",
        "update_stmt_ids",
    }


def test_dashboard_agent_contract():
    agent = DashboardAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "dashboard"
    assert "dashboard specs" in agent.description
    assert tool_names == {
        "build_dashboard_spec",
        "serve_dashboard",
        "dashboard_playbook",
    }


def test_api_keys_agent_contract():
    agent = ApiKeysAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "api_keys"
    assert "API key" in agent.description
    assert tool_names == {
        "list_api_keys",
        "create_api_key",
        "update_api_key",
        "delete_api_key",
    }


def test_users_agent_contract():
    agent = UsersAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "users"
    assert "user" in agent.description.lower()
    assert tool_names == {
        "list_users",
        "create_user",
        "get_user_by_id",
        "update_user",
        "delete_user",
        "deactivate_user",
        "reactivate_user",
        "resend_user_invitation",
        "get_user_preferences",
        "update_user_preferences",
        "get_user_organizations",
    }


def test_context_agent_contract():
    agent = ContextAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "context"
    assert "context" in agent.description.lower()
    assert tool_names == {
        "get_context",
    }


def test_exports_agent_contract():
    agent = ExportsAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "exports"
    assert "export" in agent.description.lower()
    assert tool_names == {
        "list_exports",
        "create_export",
        "get_export",
        "delete_export",
    }


def test_usage_agent_contract():
    agent = UsageAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "usage"
    assert "usage" in agent.description.lower()
    assert tool_names == {
        "get_usage_for_log_id",
        "get_usage_for_user_per_log_id",
    }


def test_forward_agent_contract():
    agent = ForwardAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "forward"
    assert "forward" in agent.description.lower()
    assert tool_names == {
        "list_forward_configs",
        "create_forward_config",
        "update_forward_config",
        "delete_forward_config",
        "test_forward_destination",
    }


def test_groups_agent_contract():
    agent = GroupsAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "groups"
    assert "group" in agent.description.lower()
    assert tool_names == {
        "list_groups",
        "create_group",
        "get_group",
        "update_group",
        "delete_group",
        "list_group_members",
        "add_group_members",
        "remove_group_members",
        "list_member_groups",
    }


def test_monitors_agent_contract():
    agent = MonitorsAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "monitors"
    assert "monitor" in agent.description.lower()
    assert tool_names == {
        "list_monitors_by_log",
    }


def test_dashboards_api_agent_contract():
    agent = DashboardsApiAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "dashboards_api"
    assert "dashboard" in agent.description.lower()
    assert tool_names == {
        "list_dashboards_by_log",
    }


def test_access_agent_contract():
    agent = AccessAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "access"
    assert "access" in agent.description.lower()
    assert tool_names == {
        "grant_access",
        "revoke_access",
        "list_access_members",
        "check_access",
        "switch_active_organization",
    }


def test_tags_agent_contract():
    agent = TagsAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "tags"
    assert "tag" in agent.description.lower()
    assert tool_names == {
        "list_tags",
        "create_tag",
        "update_tag",
        "delete_tag",
    }


def test_parsers_agent_contract():
    agent = ParsersAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "parsers"
    assert "parser" in agent.description.lower()
    assert tool_names == {
        "get_parsers_usage_for_log_id",
        "get_parsers_usage_for_user_per_log_id",
    }


def test_policies_agent_contract():
    agent = PoliciesAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "policies"
    assert "polic" in agent.description.lower()
    assert tool_names == {
        "list_policies_by_resource",
    }


def test_encryption_keys_agent_contract():
    agent = EncryptionKeysAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "encryption_keys"
    assert "encryption key" in agent.description.lower()
    assert tool_names == {
        "list_encryption_keys",
        "create_encryption_key",
        "get_encryption_key",
        "update_encryption_key",
        "delete_encryption_key",
    }
