from app.core.logger import get_logger
from app.tools.tavily_tool import tavily_search

logger = get_logger(__name__)


def hotel_node(state):
    try:
        logger.info("Hotel node started")

        destination = state["destination"]
        budget = state.get("budget")

        query = f"Best hotels within 3 km of {destination} city center"

        if budget:
            query += f" within a total trip budget of {budget}"

        logger.info(f"Searching hotels with query: {query}")

        hotel_results = tavily_search(query)

        logger.info("Hotel information fetched successfully")

        return {
            "hotel_results": hotel_results
        }

    except Exception as e:
        logger.exception(f"Hotel search failed: {str(e)}")

        return {
            "hotel_results": f"Hotel search failed: {str(e)}"
        }