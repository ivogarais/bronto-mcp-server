from unittest.mock import Mock

from bronto.agents.statement_ids.tools.handlers import StatementIdsToolHandlers


class _StatementIdsRuntime(StatementIdsToolHandlers):
    def __init__(self, bronto_client):
        self.bronto_client = bronto_client


def test_create_stmt_id_returns_16_char_hex_string():
    stmt_id = StatementIdsToolHandlers.create_stmt_id()

    assert len(stmt_id) == 16
    int(stmt_id, 16)


def test_inject_stmt_ids_playbook_contains_requested_source_path():
    playbook = StatementIdsToolHandlers.inject_stmt_ids("src/project")

    assert "src/project" in playbook
    assert "stmt_id=" in playbook


def test_extract_stmt_ids_playbook_uses_default_csv_path():
    playbook = StatementIdsToolHandlers.extract_stmt_ids()

    assert "statementIds.csv" in playbook
    assert "statement_id,log_statement,file_path,line_number" in playbook


def test_update_stmt_ids_playbook_inlines_inject_and_extract_steps():
    playbook = StatementIdsToolHandlers.update_stmt_ids(
        src_path="src/app", stmt_id_filepath="tmp/statementIds.csv"
    )

    assert "Inject Statement IDs" in playbook
    assert "Extract and Refresh CSV" in playbook
    assert "src/app" in playbook
    assert "tmp/statementIds.csv" in playbook
    assert "${" not in playbook


def test_statement_ids_playbook_lists_full_workflow():
    playbook = StatementIdsToolHandlers.statement_ids_playbook()

    assert "create_stmt_id" in playbook
    assert "deploy_statements" in playbook


def test_deploy_statements_delegates_to_bronto_client():
    client = Mock()
    client.deploy_statements.return_value = {"success": True}
    runtime = _StatementIdsRuntime(client)

    result = runtime.deploy_statements(
        csv_file_path="statementIds.csv",
        project_id="bronto-mcp-server",
        version="1.0.0",
        repo_url="https://github.com/example/repo.git",
    )

    client.deploy_statements.assert_called_once_with(
        "statementIds.csv",
        "bronto-mcp-server",
        "1.0.0",
        "https://github.com/example/repo.git",
    )
    assert result == {"success": True}
