import os
import json
from typing import Any

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.core.logger import get_logger


load_dotenv()

logger = get_logger(__name__)

TAVILY_MCP_URL = os.getenv("TAVILY_MCP_URL")


client = MultiServerMCPClient(
    {
        "tavily": {
            "transport": "streamable_http",
            "url": TAVILY_MCP_URL,
        }
    }
)


SEARCH_TOOL = None


async def initialize_mcp():
    global SEARCH_TOOL

    if SEARCH_TOOL is not None:
        logger.info("MCP already initialized")
        return

    logger.info("MCP initialization started")

    tools = await client.get_tools()

    logger.info(
        "MCP tools discovered: %s",
        [tool.name for tool in tools]
    )

    for tool in tools:
        if tool.name == "tavily_search":
            SEARCH_TOOL = tool
            break

    if SEARCH_TOOL is None:
        raise RuntimeError(
            "tavily_search tool was not found."
        )

    logger.info(
        "MCP initialization completed | tool=%s",
        SEARCH_TOOL.name
    )


async def mcp_search_tool(query: str) -> dict[str, Any]:
    if SEARCH_TOOL is None:
        await initialize_mcp()

    logger.info(
        "MCP search started | query=%s",
        query
    )

    result = await SEARCH_TOOL.ainvoke(
        {"query": query}
    )

    logger.info(
        "MCP search completed"
    )

    return parse_search_result(result)


def parse_search_result(result: Any) -> dict[str, Any]:
    if not result:
        return {}

    first_result = result[0]

    if isinstance(first_result, dict):
        text = first_result.get("text")
    else:
        text = getattr(
            first_result,
            "text",
            None
        )

    if not text:
        raise RuntimeError(
            "Unable to extract text from MCP search result."
        )

    return json.loads(text)