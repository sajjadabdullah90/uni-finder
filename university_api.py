import requests
API_URL = "http://universities.hipolabs.com/search"

def search_universities(name=None, country=None):
    """Fetch universities from the Hipolabs API."""

    params = {}

    if name:
        params["name"] = name

    if country:
        params["country"] = country

    response = requests.get(
        API_URL,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    universities = response.json()

    if not isinstance(universities, list):
        raise ValueError("Unexpected API response format.")

    return universities
