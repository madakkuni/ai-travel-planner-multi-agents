import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
API_URL = os.getenv("AVIATIONSTACK_API_URL")

def search_flights(query):
    params = {"access_key": API_KEY, "limit": 5}
    response = requests.get(API_URL, params=params)
    data = response.json()
    flights = []

    if "data" in data:
        for flight in data["data"][:5]:
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

    return "\n\n".join(flights)


if __name__ == "__main__":
    result = search_flights("flights from Bangalore to Delhi")
    print(result)