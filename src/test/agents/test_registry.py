from bronto.agents import build_agent_registry


def test_build_agent_registry_contains_all_agents():
    registry = build_agent_registry()
    names = {agent.name for agent in registry.agents}
    assert names == {"search", "datasets", "statement_ids"}


def test_registered_tools_have_unique_names_and_match_handlers():
    registry = build_agent_registry()
    tools = list(registry.iter_tool_specs())
    names = [tool.name for tool in tools]

    assert len(names) == len(set(names))
    assert all(tool.name == tool.handler for tool in tools)
