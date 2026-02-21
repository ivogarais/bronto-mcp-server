from enum import Enum
from typing import Iterable

from pydantic import BaseModel, Field, model_validator


class AgentKind(str, Enum):
    TOOL = "tool"
    PROMPT = "prompt"


class ToolExecutionSpec(BaseModel):
    required_inputs: list[str] = Field(default_factory=list)
    expected_output: str = Field(default="")
    notes: str = Field(default="")

    @model_validator(mode="after")
    def validate_payload(self) -> "ToolExecutionSpec":
        if not self.expected_output:
            raise ValueError("execution.expected_output must be set")
        return self


class AgentToolSpec(BaseModel):
    name: str = Field(description="Tool or prompt name exposed to MCP clients")
    handler: str = Field(
        description="Method name on BrontoTools that implements this spec"
    )
    kind: AgentKind = Field(default=AgentKind.TOOL)
    description: str = Field(description="LLM-facing tool description")
    execution: ToolExecutionSpec = Field(
        description="Execution contract used for validation and discovery"
    )


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
