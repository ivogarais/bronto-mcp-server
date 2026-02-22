from bronto.agents.api_keys import ApiKeysAgent
from bronto.agents.context import ContextAgent
from bronto.agents.dashboard import DashboardAgent
from bronto.agents.datasets import DatasetsAgent
from bronto.agents.exports import ExportsAgent
from bronto.agents.forward import ForwardAgent
from bronto.agents.search import SearchAgent
from bronto.agents.statement_ids import StatementIdsAgent
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
