from fastapi import FastAPI

from app.api.travel_route import router as travel_router


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