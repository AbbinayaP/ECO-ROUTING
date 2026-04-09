import os
from datetime import datetime
from typing import Dict, Any

import requests

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
GOOGLE_DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json"


class RoutingError(Exception):
    pass


def get_route_from_google(
    origin: str,
    destination: str,
    mode: str,
    use_traffic: bool = True,
) -> Dict[str, Any]:
    if not GOOGLE_MAPS_API_KEY:
        raise RoutingError("GOOGLE_MAPS_API_KEY is not configured")

    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "key": GOOGLE_MAPS_API_KEY,
    }

    if use_traffic and mode in {"driving", "bicycling"}:
        params["departure_time"] = "now"
        params["traffic_model"] = "best_guess"

    if mode == "transit":
        params["transit_mode"] = "rail|bus"

    response = requests.get(GOOGLE_DIRECTIONS_URL, params=params, timeout=10)
    data = response.json()

    if data.get("status") != "OK":
        raise RoutingError(f"Google Directions API error: {data.get('status')}")

    route = data["routes"][0]
    leg = route["legs"][0]

    distance_m = leg["distance"]["value"]
    duration_s = leg["duration"]["value"]
    duration_in_traffic_s = leg.get("duration_in_traffic", leg["duration"])["value"]
    polyline = route["overview_polyline"]["points"]

    distance_km = distance_m / 1000.0
    duration_min = duration_s / 60.0
    duration_in_traffic_min = duration_in_traffic_s / 60.0
    traffic_delay_min = max(duration_in_traffic_min - duration_min, 0.0)

    # Extract step details
    import re
    def clean_html(raw_html: str) -> str:
        # Replace tags with a space to avoid joining words like "southRestricted"
        cleanr = re.compile("<.*?>")
        cleantext = re.sub(cleanr, " ", raw_html)
        # Remove extra spaces
        return " ".join(cleantext.split())

    steps = []
    for s in leg.get("steps", []):
        step_data = {
            "instruction": clean_html(s.get("html_instructions", "")),
            "distance": s.get("distance", {}).get("text", ""),
            "duration": s.get("duration", {}).get("text", ""),
            "mode": s.get("travel_mode", "").lower(),
        }
        
        if s.get("travel_mode") == "TRANSIT":
            transit_details = s.get("transit_details", {})
            step_data["transit_line"] = transit_details.get("line", {}).get("short_name") or transit_details.get("line", {}).get("name")
            step_data["departure_stop"] = transit_details.get("departure_stop", {}).get("name")
            step_data["arrival_stop"] = transit_details.get("arrival_stop", {}).get("name")
            
        steps.append(step_data)

    return {
        "origin": leg["start_address"],
        "destination": leg["end_address"],
        "distance_km": distance_km,
        "duration_min": duration_min,
        "duration_in_traffic_min": duration_in_traffic_min,
        "traffic_delay_min": traffic_delay_min,
        "polyline": polyline,
        "steps": steps,
        "raw": data,
        "fetched_at": datetime.utcnow().isoformat(),
    }

