from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.logger import get_logger
from app.services.travel_service import process_travel_request

logger = get_logger(__name__)

router = APIRouter()


class TravelRequest(BaseModel):
    user_query: str


@router.post("/travel")
def create_travel_plan(request: TravelRequest):
    try:
        logger.info("Travel API request received")

        result = process_travel_request(request.user_query)

        logger.info("Travel API request completed successfully")

        return result

    except Exception as e:
        logger.exception(f"Travel API request failed: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Unable to process travel request"
        )