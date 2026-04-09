import requests
import json
import time

url = "http://127.0.0.1:8000/api/routes/compute"

def test_algorithm(algo_name):
    payload = {
        "origin": "Malleswaram, Bangalore",
        "destination": "Koramangala, Bangalore",
        "modes": ["car"],
        "vehicle_type": "car",
        "fuel_type": "petrol",
        "algorithm": algo_name
    }
    print(f"\n--- Testing Algorithm: {algo_name.upper()} ---")
    
    start_time = time.time()
    try:
        response = requests.post(url, json=payload)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            options = data.get("options", [])
            if options:
                route = options[0]
                print(f"Distance: {route['distance_km']:.2f} km")
                print(f"Time: {route['duration_min']:.2f} min")
                print(f"CO2 Emissions: {route['co2_kg']:.2f} kg")
            print(f"API Computation Time: {end_time - start_time:.2f} seconds")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Connection Error: {e}")

test_algorithm("astar")
test_algorithm("multi_objective")
