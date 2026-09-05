from app.core.logger import get_logger

logger = get_logger(__name__)


AIRPORT_CODES = {
    "bangalore": "BLR",
    "bengaluru": "BLR",
    "calicut": "CCJ",
    "kozhikode": "CCJ",
    "delhi": "DEL",
    "mumbai": "BOM",
    "chennai": "MAA",
    "hyderabad": "HYD",
    "kolkata": "CCU"
}


def get_airport_code(city):
    city_name = city.strip().lower()

    airport_code = AIRPORT_CODES.get(city_name)

    if not airport_code:
        logger.error(f"Airport code not found for city: {city}")
        raise ValueError(f"Airport code not found for city: {city}")

    logger.info(f"Airport code resolved: {city} -> {airport_code}")

    return airport_code