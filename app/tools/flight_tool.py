import os

import requests
from dotenv import load_dotenv

from app.tools.airport_tool import get_airport_code

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
API_URL = os.getenv("AVIATIONSTACK_API_URL")


def search_flights(origin, destination, departure_date, adults, children):
    try:
        origin_code = get_airport_code(origin)
        destination_code = get_airport_code(destination)

        params = {
            "access_key": API_KEY,
            "dep_iata": origin_code,
            "arr_iata": destination_code,
            "flight_status": "scheduled",
            "limit": 5
        }

        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        flights = []

        for flight in data.get("data", []):
            airline = flight.get("airline", {}).get("name", "Unknown")
            departure = flight.get("departure", {}).get("airport", "Unknown")
            departure_time = flight.get("departure", {}).get("scheduled", "Unknown")
            arrival = flight.get("arrival", {}).get("airport", "Unknown")
            arrival_time = flight.get("arrival", {}).get("scheduled", "Unknown")
            status = flight.get("flight_status", "Unknown")

            flights.append(
                f"Airline: {airline}\n"
                f"Departure: {departure}\n"
                f"Departure Time: {departure_time}\n"
                f"Arrival: {arrival}\n"
                f"Arrival Time: {arrival_time}\n"
                f"Status: {status}"
            )

        if not flights:
            return f"No scheduled flights found from {origin} to {destination}"

        return "\n\n".join(flights)

    except (requests.RequestException, ValueError) as e:
        raise RuntimeError(f"Flight search failed: {str(e)}")