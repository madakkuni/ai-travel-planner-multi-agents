from langgraph.graph import StateGraph, START, END
from app.nodes.flight_node import flight_node
from app.nodes.hotel_node import hotel_node
from app.graph.state import TravelState
from app.core.logger import get_logger

logger = get_logger(__name__)

def create_travel_graph():
    try:
        logger.info("Creating travel planning graph")

        graph = StateGraph(TravelState)

        # Define the nodes in the graph
        graph.add_node("flight_node", flight_node)
        graph.add_node("hotel_node", hotel_node)

        # Define the edges between nodes
        graph.add_edge(START, "flight_node")
        graph.add_edge("flight_node", "hotel_node")
        graph.add_edge("hotel_node", END)

        app = graph.compile()

        logger.info("Travel planning graph created successfully")

        return app
    except Exception as e:
        logger.exception(f"Failed to create travel booking graph: {str(e)}")
        raise
