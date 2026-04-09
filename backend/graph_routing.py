import osmnx as ox
import networkx as nx
from geopy.distance import geodesic
import time
from typing import Dict, Any, List, Tuple
import os
import pickle

# Cache directory for the city graph
CACHE_DIR = "data/graphs"
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_FILE = os.path.join(CACHE_DIR, "bangalore_graph.pkl")


def get_city_graph(place_name="Bangalore, India"):
    """
    Loads or downloads the road network graph for the given place.
    """
    if os.path.exists(CACHE_FILE):
        print(f"Loading graph from cache: {CACHE_FILE}")
        try:
            with open(CACHE_FILE, "rb") as f:
                G = pickle.load(f)
            return G
        except Exception as e:
            print(f"Error loading cache: {e}. Re-downloading...")

    print(f"Downloading graph for {place_name}...")
    # 'drive' network type handles driving routing
    G = ox.graph_from_place(place_name, network_type="drive", simplify=True)
    
    # Impute missing edge speeds and travel times
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)
    
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(G, f)
    
    print("Graph downloaded and cached.")
    return G


def find_nearest_node(G, lat: float, lng: float):
    """
    Finds the nearest node in the graph to the given coordinates.
    """
    # OSMnx uses (y, x) for coords logic, ox.distance.nearest_nodes takes (G, X, Y)
    return ox.distance.nearest_nodes(G, X=lng, Y=lat)


def compute_dijkstra(G, source_node, target_node, weight="travel_time") -> Tuple[List[int], float]:
    """
    Computes the shortest path using Dijkstra's algorithm.
    """
    try:
        path = nx.dijkstra_path(G, source=source_node, target=target_node, weight=weight)
        cost = nx.dijkstra_path_length(G, source=source_node, target=target_node, weight=weight)
        return path, cost
    except nx.NetworkXNoPath:
        return [], float('inf')


def compute_astar(G, source_node, target_node, weight="travel_time") -> Tuple[List[int], float]:
    """
    Computes the shortest path using the A* algorithm.
    """
    target_y = G.nodes[target_node]['y']
    target_x = G.nodes[target_node]['x']

    def heuristic(u, v):
        # Haversine distance from node u to target_node
        # Note: v is the target in A* heuristic call, but we can ignore it since networkx 
        # calls heuristic(node, target), so u=node, v=target.
        u_y = G.nodes[u]['y']
        u_x = G.nodes[u]['x']
        # Distance in meters / assumed speed (e.g., 50 km/h = ~13.8 m/s) to get seconds
        dist_m = geodesic((u_y, u_x), (target_y, target_x)).meters
        # Assuming an average high speed to ensure the heuristic is admissible
        # Weighting by travel_time requires heuristic in seconds
        return dist_m / 15.0  

    try:
        path = nx.astar_path(G, source=source_node, target=target_node, heuristic=heuristic, weight=weight)
        cost = nx.astar_path_length(G, source=source_node, target=target_node, heuristic=heuristic, weight=weight)
        return path, cost
    except nx.NetworkXNoPath:
        return [], float('inf')


def compute_multi_objective_astar(G, source_node, target_node, alpha=0.5, beta=0.5) -> Tuple[List[int], float]:
    """
    Computes a Multi-Objective shortest path.
    Cost = alpha * (normalized travel_time) + beta * (normalized edge_length)
    """
    target_y = G.nodes[target_node]['y']
    target_x = G.nodes[target_node]['x']
    
    # Define max values for normalization (approximate typical maxes per edge in urban grid)
    # This prevents distance (meters) from completely overwhelming time (seconds)
    MAX_TIME_S = 180.0
    MAX_DIST_M = 1000.0

    def heuristic(u, v):
        u_y = G.nodes[u]['y']
        u_x = G.nodes[u]['x']
        dist_m = geodesic((u_y, u_x), (target_y, target_x)).meters
        # Assuming 15 m/s (~50 km/h) max to ensure admissibility for time
        time_s = dist_m / 15.0 
        
        norm_time = time_s / MAX_TIME_S
        norm_dist = dist_m / MAX_DIST_M
        return (alpha * norm_time) + (beta * norm_dist)
        
    def mo_weight(u, v, d):
        time_s = d.get('travel_time', 0.0)
        dist_m = d.get('length', 0.0)
        
        norm_time = time_s / MAX_TIME_S
        norm_dist = dist_m / MAX_DIST_M
        return (alpha * norm_time) + (beta * norm_dist)

    try:
        path = nx.astar_path(G, source=source_node, target=target_node, heuristic=heuristic, weight=mo_weight)
        # Recalculate true time cost using standard weight for reporting
        cost = nx.path_weight(G, path, weight="travel_time") 
        return path, cost
    except nx.NetworkXNoPath:
        return [], float('inf')


def extract_path_metrics(G, path: List[int]) -> Dict[str, Any]:
    """
    Extracts metrics (distance, geometry) from a computed path.
    """
    if not path:
        return {"distance_km": 0.0, "duration_min": 0.0, "polyline": []}

    total_distance_m = 0.0
    total_travel_time_s = 0.0
    polyline = []
    
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i+1]
        
        # Sometimes there are multiple edges between nodes in a MultiDiGraph
        # We take the shortest one
        edge_data = min(G.get_edge_data(u, v).values(), key=lambda d: d.get('travel_time', float('inf')))
        
        total_distance_m += edge_data.get('length', 0.0)
        total_travel_time_s += edge_data.get('travel_time', 0.0)
        
        # Get geometry if available, else just node coordinates
        if 'geometry' in edge_data:
            # Shapely LineString coords
            coords = list(edge_data['geometry'].coords)
            # Convert to [lat, lng] format for frontend polyline
            polyline.extend([{"lat": lat, "lng": lon} for lon, lat in coords])
        else:
            u_node = G.nodes[u]
            v_node = G.nodes[v]
            polyline.append({"lat": u_node['y'], "lng": u_node['x']})
            if i == len(path) - 2: # Append last node
                 polyline.append({"lat": v_node['y'], "lng": v_node['x']})

    # Remove consecutive duplicate points
    if polyline:
        clean_polyline = [polyline[0]]
        for pt in polyline[1:]:
             if pt["lat"] != clean_polyline[-1]["lat"] or pt["lng"] != clean_polyline[-1]["lng"]:
                 clean_polyline.append(pt)
        polyline = clean_polyline

    # To be compatible with frontend polyline rendering logic, we might need a string encoder
    # But let's return a list of dicts or just standard list, and handle polyline encoding in main.py
    # or just return list of {"lat":..., "lng":...}

    return {
        "distance_km": total_distance_m / 1000.0,
        "duration_min": total_travel_time_s / 60.0,
        "polyline": polyline
    }

def get_route_from_graph(G, origin_lat: float, origin_lng: float, dest_lat: float, dest_lng: float, algorithm: str):
    source_node = find_nearest_node(G, origin_lat, origin_lng)
    target_node = find_nearest_node(G, dest_lat, dest_lng)
    
    if algorithm == "dijkstra":
        path, cost = compute_dijkstra(G, source_node, target_node)
    elif algorithm == "astar":
        path, cost = compute_astar(G, source_node, target_node)
    elif algorithm == "multi_objective":
        # 50% Time / 50% Distance (Emissions proxy) weighting
        path, cost = compute_multi_objective_astar(G, source_node, target_node, alpha=0.5, beta=0.5)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
        
    metrics = extract_path_metrics(G, path)
    return metrics
