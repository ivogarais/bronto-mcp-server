from enum import Enum
from typing import Any, Iterable

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AgentKind(str, Enum):
    TOOL = "tool"
    PROMPT = "prompt"


class ToolInputSpec(BaseModel):
    name: str = Field(description="Input argument name exposed by the tool")
    value_type: Any = Field(
        default=Any, description="Python type accepted for this input argument"
    )
    required: bool = Field(default=True)
    description: str = Field(default="")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="after")
    def validate_payload(self) -> "ToolInputSpec":
        if not self.name:
            raise ValueError("execution.inputs[].name must be set")
        return self


class ToolOutputSpec(BaseModel):
    value_type: Any = Field(default=Any, description="Python type returned by the tool")
    description: str = Field(default="")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ToolExecutionSpec(BaseModel):
    inputs: list[ToolInputSpec] = Field(default_factory=list)
    output: ToolOutputSpec = Field(default_factory=ToolOutputSpec)
    notes: str = Field(default="")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="after")
    def validate_payload(self) -> "ToolExecutionSpec":
        known_inputs: set[str] = set()
        for input_spec in self.inputs:
            if input_spec.name in known_inputs:
                raise ValueError(f"execution.inputs contains duplicate input: {input_spec.name}")
            known_inputs.add(input_spec.name)
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
