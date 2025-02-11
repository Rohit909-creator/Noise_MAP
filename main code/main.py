import folium
import googlemaps
import requests
import random

# Function to fetch nearby events using Google Places API
def fetch_nearby_events(api_key, location, radius=5000, keyword="event hall|auditorium|grounds"):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{location[0]},{location[1]}",
        "radius": radius,
        "keyword": keyword,
        "key": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        events = []
        for place in data.get("results", []):
            name = place.get("name")
            address = place.get("vicinity")
            rating = place.get("rating", "No rating")
            latitude = place["geometry"]["location"]["lat"]
            longitude = place["geometry"]["location"]["lng"]
            events.append((name, address, rating, latitude, longitude))
        return events
    else:
        print("Error fetching events:", response.status_code)
        return []

# Function to generate random noise data points
def generate_noise_data(center_lat, center_lng, count):
    noise_data = []
    for _ in range(count):
        random_lat = center_lat + random.uniform(-0.05, 0.05)
        random_lng = center_lng + random.uniform(-0.05, 0.05)
        random_noise = random.randint(40, 100)  # Noise levels in dB (40-100)
        noise_data.append((random_lat, random_lng, random_noise))
    return noise_data

# Initialize Google Maps client with your API key
api_key = "AIzaSyA1Kz-U4z5JTBOLDFGQQKAYTwZzPLaxF6E"  # Replace with your API key
gmaps = googlemaps.Client(key=api_key)

# Define start and end locations
start_location = "Delhi, India"
end_location = "Noida, India"

# Get the latitude and longitude for the start location
start_geocode = gmaps.geocode(start_location)
start_coords = start_geocode[0]['geometry']['location']
start_lat = start_coords['lat']
start_lng = start_coords['lng']

# Get the latitude and longitude for the end location
end_geocode = gmaps.geocode(end_location)
end_coords = end_geocode[0]['geometry']['location']
end_lat = end_coords['lat']
end_lng = end_coords['lng']

# Create a Folium map centered at the midpoint between start and end locations
mid_lat = (start_lat + end_lat) / 2
mid_lng = (start_lng + end_lng) / 2
mymap = folium.Map(location=[mid_lat, mid_lng], zoom_start=12)

# Add start and end markers
folium.Marker(location=[start_lat, start_lng], popup="Start: Delhi", icon=folium.Icon(color="green")).add_to(mymap)
folium.Marker(location=[end_lat, end_lng], popup="End: Noida", icon=folium.Icon(color="red")).add_to(mymap)

# Fetch and add events near the start location
start_events = fetch_nearby_events(api_key, (start_lat, start_lng))
for name, address, rating, lat, lng in start_events:
    folium.Marker(
        location=[lat, lng],
        popup=f"Event: {name}\nAddress: {address}\nRating: {rating}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(mymap)

# Fetch and add events near the end location
end_events = fetch_nearby_events(api_key, (end_lat, end_lng))
for name, address, rating, lat, lng in end_events:
    folium.Marker(
        location=[lat, lng],
        popup=f"Event: {name}\nAddress: {address}\nRating: {rating}",
        icon=folium.Icon(color="purple", icon="info-sign")
    ).add_to(mymap)

# Generate and add noise data points near the start location
start_noise = generate_noise_data(start_lat, start_lng, 20)
for lat, lng, noise_level in start_noise:
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

# Generate and add noise data points near the end location
end_noise = generate_noise_data(end_lat, end_lng, 20)
for lat, lng, noise_level in end_noise:
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
mymap.save("events_and_noise_map.html")

# Print success message
print("Map with events and noise data saved as 'events_and_noise_map.html'. Open this file to view the map.")
