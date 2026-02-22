from bronto.agents.dashboard import DashboardAgent
from bronto.agents.datasets import DatasetsAgent
from bronto.agents.search import SearchAgent
from bronto.agents.statement_ids import StatementIdsAgent


def test_datasets_agent_contract():
    agent = DatasetsAgent()
    tool_names = {tool.name for tool in agent.tools}

    assert agent.name == "datasets"
    assert "Discovers datasets" in agent.description
    assert tool_names == {
        "get_datasets",
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
