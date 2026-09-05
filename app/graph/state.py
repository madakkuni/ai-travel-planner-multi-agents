# State

from typing import TypedDict, Annotated
import operator
from langchain_core.messages import (AnyMessage, HumanMessage, AIMessage, SystemMessage,)

class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int
    error: str