import uuid

from langchain_core.messages import HumanMessage

from app.core.logger import get_logger
from app.graph.workflow import create_travel_graph

logger = get_logger(__name__)


def process_travel_request(user_query):
    try:
        logger.info("Processing travel request")

        thread_id = str(uuid.uuid4())

        logger.info(f"Generated thread ID: {thread_id}")

        app = create_travel_graph()

        config = {"configurable": {"thread_id": thread_id}}

        initial_state = {
            "messages": [HumanMessage(content=user_query)],
            "user_query": user_query,
            "origin": None,
            "destination": None,
            "duration_days": None,
            "departure_date": None,
            "adults": 1,
            "children": 0,
            "budget": None,
            "flight_results": "",
            "hotel_results": ""
        }

        result = app.invoke(initial_state, config=config)

        logger.info("Travel request processed successfully")

        return {
            "thread_id": thread_id,
            "flight_results": result.get("flight_results", ""),
            "hotel_results": result.get("hotel_results", "")
        }

    except Exception as e:
        logger.exception(f"Travel request processing failed: {str(e)}")
        raise RuntimeError(f"Travel request failed: {str(e)}")