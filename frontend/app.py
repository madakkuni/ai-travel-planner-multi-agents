import os

import httpx
import streamlit as st


st.set_page_config(
    page_title="AI travel planner",
    page_icon=":material/luggage:",
    layout="centered",
)

st.title("AI travel planner")
st.write("Describe your trip and get flight and hotel suggestions.")

api_url = os.getenv("TRAVEL_API_URL", "http://localhost:8000").rstrip("/")

with st.form("travel_request"):
    user_query = st.text_area(
        "Your travel request",
        placeholder="Plan a 5-day trip from Bangalore to Calicut for 1 adult",
        height=120,
    )
    submitted = st.form_submit_button(
        "Plan my trip",
        type="primary",
        icon=":material/search:",
        width="stretch",
    )

if submitted:
    if not user_query.strip():
        st.warning("Enter a travel request first.")
    else:
        try:
            with st.spinner("Planning your trip..."):
                response = httpx.post(
                    f"{api_url}/travel",
                    json={"user_query": user_query.strip()},
                    timeout=120.0,
                )
            response.raise_for_status()
            result = response.json()

            st.success("Travel plan generated")
            st.caption(f"Thread ID: {result.get('thread_id', 'Unavailable')}")

            with st.container(border=True):
                st.subheader("Flights")
                st.write(result.get("flight_results") or "No flight results returned.")

            with st.container(border=True):
                st.subheader("Hotels")
                st.write(result.get("hotel_results") or "No hotel results returned.")

        except httpx.HTTPStatusError as error:
            detail = error.response.text or "The API returned an error."
            st.error(f"API error ({error.response.status_code}): {detail}")
        except httpx.RequestError:
            st.error(
                f"Could not connect to the API at {api_url}. "
                "Start the FastAPI server and try again."
            )
        except ValueError:
            st.error("The API returned an invalid JSON response.")