from fastapi import FastAPI

from app.core.logger import get_logger, setup_logging
from app.api.travel_route import router as travel_router


setup_logging()
logger = get_logger(__name__)
logger.info("Application started")


# Create the FastAPI application.
app = FastAPI(
    title="AI Travel Planner Multi Agents",
    version="0.1.0",
    description="AI-powered multi-agent travel planning application.",
)


# Provide a basic application status endpoint.
@app.get("/")
def root():
    return {
        "message": "AI Travel Planner Multi Agents API is running."
    }


# Register the travel API routes.
app.include_router(travel_router)