from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from app.core.logger import setup_logging, get_logger
from app.graph.workflow import create_travel_graph

load_dotenv()
setup_logging()

logger = get_logger(__name__)


def main():
    try:
        logger.info("Travel planner application started")

        app = create_travel_graph()

        user_input = input("Enter your travel request: ")

        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "user_query": user_input,
            "origin": "",
            "destination": "",
            "duration_days": 0,
            "departure_date": None,
            "adults": 1,
            "children": 0,
            "budget": None,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0,
            "error": ""
        }

        result = app.invoke(initial_state)

        print("\nFLIGHT RESULTS:")
        print(result["flight_results"])

        print("\nHOTEL RESULTS:")
        print(result["hotel_results"])

        if result["error"]:
            print("\nERROR:")
            print(result["error"])

        logger.info("Travel planner application completed successfully")

    except Exception as e:
        logger.exception(f"Application failed: {e}")
        print(f"\nApplication error: {e}")


if __name__ == "__main__":
    main()