import folium
import googlemaps
from googlemaps.convert import decode_polyline
import random
import math

def generate_sound_data_along_routes(route_coords, count):
    """Generate random sound data points along the route."""
    noise_data = []
    total_segments = len(route_coords) - 1
    points_per_segment = count // total_segments

    for i in range(total_segments):
        start = route_coords[i]
        end = route_coords[i + 1]
        for _ in range(points_per_segment):
            # Interpolate a point between start and end
            t = random.uniform(0, 1)  # Random factor between 0 and 1
            lat = start[0] + t * (end[0] - start[0])
            lng = start[1] + t * (end[1] - start[1])

            # Generate random noise level
            noise_level = random.randint(40, 100)  # Noise levels in dB (40-100)
            noise_data.append((lat, lng, noise_level))
    return noise_data

# Initialize Google Maps client with your API key
api_key = "AIzaSyA1Kz-U4z5JTBOLDFGQQKAYTwZzPLaxF6E"  # Replace with your actual API key
gmaps = googlemaps.Client(key=api_key)

# Define start and end locations
start_location = "Trivandrum, India"
end_location = "Kochi, India"

# Request directions with alternatives enabled
directions = gmaps.directions(
    origin=start_location,
    destination=end_location,
    mode="driving",
    alternatives=True
)

# Create a Folium map centered at the start location
start_lat = directions[0]['legs'][0]['start_location']['lat']
start_lng = directions[0]['legs'][0]['start_location']['lng']
mymap = folium.Map(location=[start_lat, start_lng], zoom_start=8)

# Add all possible routes to the map and generate sound data
colors = ["blue", "green", "purple", "orange", "red"]  # Colors for different routes

for idx, route in enumerate(directions):
    # Extract the route geometry (polyline)
    route_polyline = route['overview_polyline']['points']

    # Decode the polyline into (latitude, longitude) pairs
    route_coords = decode_polyline(route_polyline)
    route_coords = [[d['lat'], d['lng']] for d in route_coords]

    # Add the route to the map
    folium.PolyLine(
        locations=route_coords,
        color=colors[idx % len(colors)],
        weight=5,
        tooltip=f"Route {idx + 1}"
    ).add_to(mymap)

    # Generate sound data along this route
    sound_data = generate_sound_data_along_routes(route_coords, 100)

    # Add sound data points to the map
    for lat, lng, noise_level in sound_data:
        if noise_level <= 60:
            marker_color = 'green'  # Low noise
        elif 60 < noise_level <= 80:
            marker_color = 'orange'  # Moderate noise
        else:
            marker_color = 'red'  # High noise

        folium.CircleMarker(
            location=[lat, lng],
            radius=4,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.7,
            popup=f"Noise Level: {noise_level} dB"
        ).add_to(mymap)

# Add start and end markers
folium.Marker(location=[start_lat, start_lng], popup="Start: Trivandrum").add_to(mymap)
end_lat = directions[0]['legs'][0]['end_location']['lat']
end_lng = directions[0]['legs'][0]['end_location']['lng']
folium.Marker(location=[end_lat, end_lng], popup="End: Kochi").add_to(mymap)

# Save the map to an HTML file
mymap.save("google_routes_noise_map.html")

# Print success message
print("Map with noise data mapped along routes saved as 'google_routes_noise_map.html'. Open this file to view the map.")
