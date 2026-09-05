from typing import TypedDict, Annotated
import operator

from langchain_core.messages import AnyMessage


class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    origin: str
    destination: str
    duration_days: int
    departure_date: str | None
    adults: int
    children: int
    budget: float | None
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int
    error: str