TRAVEL_DETAILS_PROMPT = """
Extract the travel details from the user request.

User request:
{query}

Mandatory fields:

* origin
* destination
* duration_days

Optional fields:

* departure_date
* adults
* children
* budget

Rules:

* Extract information only from the user's request.
* Do not invent or assume information that is not provided.
* If departure_date is not provided, return null.
* If adults is not provided, return 1.
* If children is not provided, return 0.
* If budget is not provided, return null.
  """
