import os
from dotenv import load_dotenv
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from typing import Any
import json   

load_dotenv()

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


# Connect to the MCP server and discover available tools.
async def initialize_mcp() -> None:
    global SEARCH_TOOL

    tools = await client.get_tools()

    print("Available MCP tools:")

    for tool in tools:
        print(f"Tool: {tool.name}, Description: {tool.description}")

        if tool.name == "tavily_search":
            SEARCH_TOOL = tool

    if SEARCH_TOOL is None:
        raise RuntimeError("tavily_search tool was not found.")

    print(f"Search tool initialized: {SEARCH_TOOL.name}")


# Execute the Tavily search tool.
async def mcp_search_tool(query: str) -> Any:
    if SEARCH_TOOL is None:
        await initialize_mcp()

    search_arguments = {"query": query}

    result = await SEARCH_TOOL.ainvoke(search_arguments)

    return parse_search_result(result)

# Convert MCP TextContent into Python dictionary.
def parse_search_result(result: Any) -> dict[str, Any]:

    if not result:
        return {}

    first_result = result[0]

    # MCP result returned as dictionary.
    if isinstance(first_result, dict):
        text = first_result.get("text")

    # MCP result returned as TextContent object.
    else:
        text = getattr(first_result, "text", None)

    if not text:
        raise RuntimeError(
            "Unable to extract text from MCP search result."
        )

    return json.loads(text)