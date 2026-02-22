import pytest

from bronto.agents.playbooks import compose_playbook, resolve_playbook


def test_resolve_playbook_loads_markdown_content():
    content = resolve_playbook(
        "bronto.agents.datasets", "playbooks/datasets_playbook.md"
    )

    assert "Datasets playbook" in content
    assert "get_datasets" in content


def test_compose_playbook_substitutes_template_variables():
    content = compose_playbook(
        "bronto.agents.statement_ids",
        "playbooks/update_stmt_ids_playbook.md",
        src_path="src/",
        stmt_id_filepath="statementIds.csv",
        inject_playbook="inject-block",
        extract_playbook="extract-block",
    )

    assert "inject-block" in content
    assert "extract-block" in content
    assert "${" not in content


def test_resolve_playbook_raises_runtime_error_for_missing_resource():
    with pytest.raises(RuntimeError, match="Cannot load playbook"):
        resolve_playbook("bronto.agents.datasets", "playbooks/does_not_exist.md")
