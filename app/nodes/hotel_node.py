import asyncio

from app.core.logger import get_logger
from app.mcp.mcp_client import mcp_search_tool


logger = get_logger(__name__)


def hotel_node(state):
    try:
        logger.info("Hotel node started")

        destination = state["destination"]
        budget = state.get("budget")

        query = f"Best hotels in {destination} city center"

        if budget:
            query += f" within a budget of {budget}"

        logger.info("Searching hotels with query: %s", query)

        search_response = asyncio.run(
            mcp_search_tool(query)
        )

        results = search_response.get("results", [])

        hotels = []

        for result in results:
            hotels.append(
                {
                    "name": result.get("title"),
                    "description": result.get("content", "")[:500],
                    "url": result.get("url"),
                }
            )

        logger.info(
            "Hotel information fetched successfully | count=%s",
            len(hotels),
        )

        return {
            "hotel_results": hotels
        }

    except Exception as e:
        logger.exception("Hotel search failed")

        return {
            "hotel_results": [],
            "hotel_error": str(e),
        }