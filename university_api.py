
import json
from pathlib import Path

import requests


API_URL = "http://universities.hipolabs.com/search"
BACKUP_FILE = Path(__file__).parent / "data" / "backup_universities.json"


def load_backup(name=None, country=None):
    """Load and filter universities from the local backup file."""

    try:
        with open(BACKUP_FILE, "r", encoding="utf-8") as file:
            universities = json.load(file)

        if not isinstance(universities, list):
            raise ValueError("Invalid backup data format.")

        if name:
            universities = [
                university for university in universities
                if name.lower() in university.get("name", "").lower()
            ]

        if country:
            universities = [
                university for university in universities
                if country.lower() in university.get("country", "").lower()
            ]

        return universities

    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Backup data unavailable: {error}")
        return []


def search_universities(name=None, country=None):
    """Fetch live university data, falling back to local data on failure."""

    params = {}

    if name:
        params["name"] = name

    if country:
        params["country"] = country

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        universities = response.json()

        if not isinstance(universities, list):
            raise ValueError("Unexpected API response format.")

        return universities

    except (requests.RequestException, ValueError) as error:
        print(f"Live API unavailable: {error}")
        print("Switching to local backup data...")

        return load_backup(name=name, country=country)
