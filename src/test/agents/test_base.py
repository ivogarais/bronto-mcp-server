from bronto.agents.base import AgentToolSpec, BrontoAgent, BrontoAgentRegistry


def test_iter_tool_specs_yields_all_tools_in_order():
    registry = BrontoAgentRegistry(
        agents=[
            BrontoAgent(
                name="a1",
                description="agent 1",
                tools=[
                    AgentToolSpec(name="t1", handler="t1", description="d1"),
                    AgentToolSpec(name="t2", handler="t2", description="d2"),
                ],
            ),
            BrontoAgent(
                name="a2",
                description="agent 2",
                tools=[AgentToolSpec(name="t3", handler="t3", description="d3")],
            ),
        ]
    )

    tool_names = [tool.name for tool in registry.iter_tool_specs()]

    assert tool_names == ["t1", "t2", "t3"]


def test_build_instructions_includes_agents_and_tools():
    registry = BrontoAgentRegistry(
        agents=[
            BrontoAgent(
                name="search",
                description="search agent",
                tools=[
                    AgentToolSpec(
                        name="search_logs", handler="search_logs", description="search"
                    )
                ],
            )
        ]
    )

    instructions = registry.build_instructions()

    assert "Available agents:" in instructions
    assert "- search: search agent" in instructions
    assert "search_logs: search" in instructions
