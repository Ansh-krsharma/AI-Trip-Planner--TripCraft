"""Live tools the agent calls instead of relying on the LLM's memory.

Both are free, keyless APIs so the project has no extra signup beyond the
LLM provider:
  - Open-Meteo for weather (https://open-meteo.com)
  - Frankfurter for currency conversion (https://frankfurter.dev)

Each function returns a small dict and never raises -- on failure it returns
{"error": "..."} so a bad network call degrades the plan instead of
crashing the graph.
"""
from __future__ import annotations

import requests

from data.guides import COORDS_BY_DESTINATION

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
CURRENCY_URL = "https://api.frankfurter.app/latest"
TIMEOUT = 8


def get_weather(destination: str) -> dict:
    """5-day forecast for a destination in the knowledge base."""
    coords = COORDS_BY_DESTINATION.get((destination or "").strip().lower())
    if not coords:
        return {
            "error": (
                f"No coordinates on file for '{destination}'. "
                f"This tool only covers destinations in the knowledge base."
            )
        }
    lat, lon = coords
    try:
        resp = requests.get(
            WEATHER_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,weather_code",
                "daily": "temperature_2m_max,temperature_2m_min,weather_code,precipitation_probability_max",
                "timezone": "auto",
                "forecast_days": 5,
            },
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        return {
            "destination": destination,
            "current_temperature_c": data.get("current", {}).get("temperature_2m"),
            "daily_max_c": data.get("daily", {}).get("temperature_2m_max"),
            "daily_min_c": data.get("daily", {}).get("temperature_2m_min"),
            "daily_rain_chance_pct": data.get("daily", {}).get("precipitation_probability_max"),
            "dates": data.get("daily", {}).get("time"),
        }
    except requests.RequestException as e:
        return {"error": f"Weather lookup failed: {e}"}


def convert_currency(amount: float, from_currency: str = "INR", to_currency: str = "USD") -> dict:
    """Convert an amount using live exchange rates."""
    try:
        resp = requests.get(
            CURRENCY_URL,
            params={"amount": amount, "from": from_currency.upper(), "to": to_currency.upper()},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        converted = data.get("rates", {}).get(to_currency.upper())
        return {
            "amount": amount,
            "from": from_currency.upper(),
            "to": to_currency.upper(),
            "converted_amount": converted,
            "date": data.get("date"),
        }
    except requests.RequestException as e:
        return {"error": f"Currency conversion failed: {e}"}
