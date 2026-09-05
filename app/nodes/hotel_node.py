from langchain_core.messages import AIMessage

from app.core.logger import get_logger
from app.tools.tavily_tool import tavily_search

logger = get_logger(__name__)


def hotel_node(state):
    try:
        logger.info("Hotel node started")

        query = f"Best hotels for {state['user_query']}"
        hotel_results = tavily_search(query)

        logger.info("Hotel information fetched successfully")

        return {
            "hotel_results": hotel_results,
            "error": "",
            "messages": [AIMessage(content="Hotel information fetched successfully")]
        }

    except Exception as e:
        error_message = f"Hotel search failed: {str(e)}"
        logger.exception(error_message)

        return {
            "hotel_results": "",
            "error": error_message,
            "messages": [AIMessage(content="Unable to fetch hotel information")]
        }