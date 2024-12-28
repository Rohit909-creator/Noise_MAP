import folium
import googlemaps
from googlemaps.convert import decode_polyline
import random
def generate_noise_data(center_lat, center_lng, count):
    noise_data = []
    for _ in range(count):
        # Generate random lat/lng near the center point
        random_lat = center_lat + (random.uniform(-0.05, 0.05))
        random_lng = center_lng + (random.uniform(-0.05, 0.05))
        random_noise = random.randint(40, 100)  # Noise levels in dB (40-100)
        noise_data.append((random_lat, random_lng, random_noise))
    return noise_data



# Initialize Google Maps client with your API key
api_key = "AIzaSyA1Kz-U4z5JTBOLDFGQQKAYTwZzPLaxF6E"  # Get it from https://console.cloud.google.com/
gmaps = googlemaps.Client(key=api_key)

# Define start and end locations
start_location = "Delhi, India"
end_location = "Noida, India"

# Request directions with alternatives enabled
directions = gmaps.directions(
    origin=start_location,
    destination=end_location,
    mode="driving",  # Options: 'driving', 'walking', 'bicycling', 'transit'
    alternatives=True  # Request multiple routes
)

# Create a Folium map centered at the start location
mymap = folium.Map(location=[28.7041, 77.1025], zoom_start=12)

# Iterate over each route and add it to the map
colors = ["blue", "green", "purple", "orange", "red"]  # Different colors for different routes
for idx, route in enumerate(directions):
    # Extract the route geometry (polyline)
    route_polyline = route['overview_polyline']['points']
    
    # Decode the polyline into (latitude, longitude) pairs
    route_coords = decode_polyline(route_polyline)
    route_coords = [[d['lat'], d['lng']] for d in route_coords]
    # Add the route to the map with a unique color
    folium.PolyLine(
        locations=route_coords,
        color=colors[idx % len(colors)],  # Cycle through colors if more routes exist
        weight=5,
        tooltip=f"Route {idx + 1}"
    ).add_to(mymap)

# Add start and end markers
folium.Marker(location=[28.7041, 77.1025], popup="Start: Delhi").add_to(mymap)
folium.Marker(location=[28.5355, 77.3910], popup="End: Noida").add_to(mymap)
noise_data = generate_noise_data(28.7041, 77.1025, 20)
for lat, lng, noise_level in noise_data:
    if noise_level <= 60:
        color = 'green'  # Low noise
    elif 60 < noise_level <= 80:
        color = 'orange'  # Moderate noise
    else:
        color = 'red'  # High noise
    
    folium.CircleMarker(
        location=[lat, lng],
        radius=7,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=f"Noise Level: {noise_level} dB"
    ).add_to(mymap)

# Save the map to an HTML file
mymap.save("google_multiple_routes_map.html")

# Print success message
print("Map with multiple routes saved as 'google_multiple_routes_map.html'. Open this file to view the map.")
