import folium
import googlemaps
from googlemaps.convert import decode_polyline
import random
import numpy as np
import json
from collections import defaultdict
from queue import PriorityQueue

# Initialize Google Maps client with your API key
api_key = "AIzaSyA1Kz-U4z5JTBOLDFGQQKAYTwZzPLaxF6E"  # Replace with a valid API key
gmaps = googlemaps.Client(key=api_key)

# Functions for simulation
def generate_noise_data(center_lat, center_lng, count):
    noise_data = []
    for _ in range(count):
        random_lat = center_lat + (random.uniform(-0.05, 0.05))
        random_lng = center_lng + (random.uniform(-0.05, 0.05))
        noise_data.append((random_lat, random_lng))
    return noise_data

def calculate_noise(route, noise_data):
    # Calculate total noise impact for a route
    total_noise = 0
    for lat, lng in route:
        for noise_lat, noise_lng in noise_data:
            distance = ((lat - noise_lat)**2 + (lng - noise_lng)**2)**0.5
            if distance < 0.01:  # Threshold for considering noise impact
                total_noise += 1 / (distance + 1e-6)
    return total_noise

def find_optimal_route(routes, noise_data):
    noise_levels = [calculate_noise(route, noise_data) for route in routes]
    optimal_index = np.argmin(noise_levels)
    return optimal_index, noise_levels

# Generate routes using Google Maps API
def generate_routes(start_location, end_location):
    directions = gmaps.directions(
        origin=start_location,
        destination=end_location,
        mode="driving",
        alternatives=True
    )
    routes = []
    for route in directions:
        route_polyline = route['overview_polyline']['points']
        route_coords = decode_polyline(route_polyline)
        routes.append([[point['lat'], point['lng']] for point in route_coords])
    return routes

# Simulate and save dataset
def simulate_dataset(start_location, end_location, noise_center, noise_count, num_samples):
    dataset = {
        "routes": [],
        "noise": [],
        "labels": []
    }
    for _ in range(num_samples):
        routes = generate_routes(start_location, end_location)
        noise_data = generate_noise_data(noise_center[0], noise_center[1], noise_count)
        optimal_index, noise_levels = find_optimal_route(routes, noise_data)
        # print(optimal_index)
        # Normalize noise levels to probabilities
        probabilities = np.exp(-np.array(noise_levels))
        # print(probabilities)
        # probabilities /= probabilities.sum()
        probabilities = [0.0 for i in range(len(probabilities.tolist()))]
        probabilities[optimal_index] = float(optimal_index)
        dataset["routes"].append(routes)
        dataset["noise"].append(noise_data)
        # dataset["labels"].append(probabilities.tolist())
        dataset["labels"].append(probabilities)
        # exit(0)
    # Save dataset as JSON
    with open("noise_routing_dataset.json", "w") as f:
        json.dump(dataset, f, indent=4)

    print("Dataset saved as 'noise_routing_dataset.json'")

# Parameters for simulation
start_location = "Delhi, India"
end_location = "Noida, India"
noise_center = [28.7041, 77.1025]
noise_count = 50
num_samples = 100

# Run simulation
simulate_dataset(start_location, end_location, noise_center, noise_count, num_samples)
