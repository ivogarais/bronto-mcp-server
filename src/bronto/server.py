from mcp.server.fastmcp import FastMCP

from bronto.agents import build_agent_registry
from bronto.clients import BrontoClient
from bronto.config import Config, MCPTransport
from bronto.logger import bootstrap_logging, module_logger
from bronto.tools import BrontoTools

logger = module_logger(__name__)


def main() -> None:
    bootstrap_logging()
    config = Config()
    logger.info("Starting Bronto MCP server, transport=%s", config.mcp_transport.value)

    agent_registry = build_agent_registry()
    mcp = FastMCP(
        "Bronto",
        host=config.mcp_host,
        port=config.mcp_port,
        stateless_http=True,
        streamable_http_path=config.mcp_streamable_http_path,
        json_response=True,
        instructions=agent_registry.build_instructions(),
        dependencies=["pydantic"],
    )
    bronto_client = BrontoClient(config.bronto_api_key, config.bronto_api_endpoint)
    bronto_tools = BrontoTools(bronto_client, agent_registry)
    bronto_tools.register(mcp)
    logger.info("Bronto tools registered successfully")
    if config.mcp_transport is MCPTransport.STREAMABLE_HTTP:
        logger.info(
            "Listening on http://%s:%s%s",
            config.mcp_host,
            config.mcp_port,
            config.mcp_streamable_http_path,
        )

    mcp.run(transport=config.mcp_transport.value)
