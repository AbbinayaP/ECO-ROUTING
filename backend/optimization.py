from typing import Dict, Any


def compare_routes(
    fastest_route: Dict[str, Any],
    eco_route: Dict[str, Any],
) -> Dict[str, float]:
    fastest_emission = fastest_route["co2_kg"]
    eco_emission = eco_route["co2_kg"]

    if fastest_emission <= 0:
        emission_saved_pct = 0.0
    else:
        emission_saved_pct = max(
            0.0, (fastest_emission - eco_emission) / fastest_emission * 100.0
        )

    time_diff_min = eco_route["duration_in_traffic_min"] - fastest_route[
        "duration_in_traffic_min"
    ]

    return {
        "emission_saved_pct": emission_saved_pct,
        "extra_travel_time_min": time_diff_min,
    }

