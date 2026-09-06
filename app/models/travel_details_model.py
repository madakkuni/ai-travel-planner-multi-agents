from pydantic import BaseModel


class TravelDetails(BaseModel):
    origin: str
    destination: str
    duration_days: int
    departure_date: str | None = None
    adults: int = 1
    children: int = 0
    budget: float | None = None