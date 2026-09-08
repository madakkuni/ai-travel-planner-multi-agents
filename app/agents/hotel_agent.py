import json

from langchain_core.messages import HumanMessage, SystemMessage

from app.core.llm import get_llm
from app.core.logger import get_logger
from app.mcp.mcp_client import mcp_search_tool
from app.prompts.hotel_extraction_prompt import HOTEL_EXTRACTION_PROMPT


logger = get_logger(__name__)


async def hotel_agent(state):
    logger.info("Hotel Agent started")

    search_query = f"Best hotels in {state['destination']}"

    raw_results = await mcp_search_tool(search_query)

    logger.info("Hotel search completed")

    messages = [
        SystemMessage(content=HOTEL_EXTRACTION_PROMPT),
        HumanMessage(
            content=json.dumps(raw_results, indent=2)
        ),
    ]

    response = get_llm().invoke(messages)

    return {
        "hotel_results": response.content
    }