from agents import AgentKind


class MCPToolRegistrationMixin:
    """Registers handlers defined on BrontoTools with MCP based on agent specs."""

    def register(self, mcp):
        for tool_spec in self.agent_registry.iter_tool_specs():
            handler = getattr(self, tool_spec.handler, None)
            if handler is None:
                raise AttributeError(f"Unknown tool handler: {tool_spec.handler}")
            if tool_spec.kind is AgentKind.PROMPT:
                mcp.prompt(name=tool_spec.name)(handler)
            else:
                mcp.tool(name=tool_spec.name, description=tool_spec.description)(
                    handler
                )
