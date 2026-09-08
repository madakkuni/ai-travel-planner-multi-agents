from langgraph.graph import END, START, StateGraph

from app.agents.hotel_agent import hotel_agent
from app.core.logger import get_logger
from app.graph.state import TravelState
from app.nodes.flight_node import flight_node
from app.nodes.travel_details_node import travel_details_node


logger = get_logger(__name__)


def create_travel_graph():
    try:
        logger.info("Creating travel planning graph")

        graph = StateGraph(TravelState)

        # Register workflow nodes.
        graph.add_node("travel_details_node", travel_details_node)
        graph.add_node("flight_node", flight_node)
        graph.add_node("hotel_agent", hotel_agent)

        # Define workflow execution order.
        graph.add_edge(START, "travel_details_node")
        graph.add_edge("travel_details_node", "flight_node")
        graph.add_edge("flight_node", "hotel_agent")
        graph.add_edge("hotel_agent", END)

        app = graph.compile()

        logger.info("Travel planning graph created successfully")

        return app

    except Exception as e:
        logger.exception("Failed to create travel planning graph")
        raise