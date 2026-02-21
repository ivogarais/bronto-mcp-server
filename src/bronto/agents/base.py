from typing import Iterable, Literal

from pydantic import BaseModel, Field


class AgentToolSpec(BaseModel):
    name: str = Field(description="Tool or prompt name exposed to MCP clients")
    handler: str = Field(
        description="Method name on BrontoTools that implements this spec"
    )
    kind: Literal["tool", "prompt"] = Field(default="tool")


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
        return "\n".join(lines)
