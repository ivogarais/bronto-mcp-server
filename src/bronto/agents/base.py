from typing import Iterable

from pydantic import BaseModel, Field


class AgentToolSpec(BaseModel):
    name: str = Field(description="Tool name exposed to MCP clients")
    handler: str = Field(
        description="Method name on BrontoRuntime that implements this spec"
    )
    description: str = Field(description="LLM-facing tool description")


class BrontoAgent(BaseModel):
    name: str = Field(description="Agent name")
    description: str = Field(description="What this agent is responsible for")
    tools: list[AgentToolSpec] = Field(default_factory=list)


class BrontoAgentRegistry(BaseModel):
    agents: list[BrontoAgent] = Field(default_factory=list)

    def iter_tool_specs(self) -> Iterable[AgentToolSpec]:
        for agent in self.agents:
            for tool in agent.tools:
                yield tool

    def build_instructions(self) -> str:
        lines = [
            "Use this MCP server to interact with Bronto datasets and log data.",
            "Available agents:",
        ]
        for agent in self.agents:
            lines.append(f"- {agent.name}: {agent.description}")
            for tool in agent.tools:
                lines.append(f"  - {tool.name}: {tool.description}")
        return "\n".join(lines)
