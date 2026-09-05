from langchain_core.messages import AIMessage

from app.core.logger import get_logger
from app.tools.flight_tool import search_flights

logger = get_logger(__name__)


def flight_node(state):
    try:
        logger.info("Flight node started")

        origin = state["origin"]
        destination = state["destination"]
        departure_date = state["departure_date"]
        adults = state["adults"]
        children = state["children"]

        logger.info(f"Searching flights from {origin} to {destination} on {departure_date}")

        flight_results = search_flights(origin, destination, departure_date, adults, children)

        logger.info("Flight information fetched successfully")

        return {
            "flight_results": flight_results,
            "error": "",
            "messages": [AIMessage(content="Flight information fetched successfully")]
        }

    except Exception as e:
        error_message = f"Flight search failed: {str(e)}"
        logger.exception(error_message)

        return {
            "flight_results": "",
            "error": error_message,
            "messages": [AIMessage(content="Unable to fetch flight information")]
        }