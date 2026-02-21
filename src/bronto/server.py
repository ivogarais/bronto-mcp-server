from mcp.server.fastmcp import FastMCP

from bronto.agents import build_agent_registry
from bronto.clients import BrontoClient
from bronto.config import Config
from bronto.logger import bootstrap_logging, module_logger
from bronto.tools import BrontoTools

logger = module_logger(__name__)


def main() -> None:
    bootstrap_logging()
    logger.info("Starting Bronto MCP server")

    agent_registry = build_agent_registry()
    mcp = FastMCP(
        "Bronto",
        stateless_http=True,
        streamable_http_path="/",
        json_response=True,
        instructions=agent_registry.build_instructions(),
        dependencies=["pydantic"],
    )
    config = Config()
    bronto_client = BrontoClient(config.bronto_api_key, config.bronto_api_endpoint)
    bronto_tools = BrontoTools(bronto_client, agent_registry)
    bronto_tools.register(mcp)
    logger.info("Bronto tools registered successfully")

    mcp.run(transport="streamable-http")
