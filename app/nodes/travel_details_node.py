from app.core.llm import get_llm
from app.core.logger import get_logger
from app.models.travel_details_model import TravelDetails
from app.prompts.travel_details_prompt import TRAVEL_DETAILS_PROMPT

logger = get_logger(__name__)

llm = get_llm()
structured_llm = llm.with_structured_output(TravelDetails)

def travel_details_node(state):
    try:
        logger.info("Travel details extraction started")

        query = state["user_query"]
        prompt = TRAVEL_DETAILS_PROMPT.format(query=query)
        travel_details = structured_llm.invoke(prompt)

        logger.info(f"Extracted travel details: {travel_details}")
        logger.info("Travel details extracted successfully")

        return {
            "origin": travel_details.origin,
            "destination": travel_details.destination,
            "duration_days": travel_details.duration_days,
            "departure_date": travel_details.departure_date,
            "adults": travel_details.adults,
            "children": travel_details.children,
            "budget": travel_details.budget,
            "llm_calls": state.get("llm_calls", 0) + 1,
            "error": ""
        }

    except Exception as e:
        error_message = f"Travel details extraction failed: {str(e)}"
        logger.exception(error_message)

        return {"error": error_message}
