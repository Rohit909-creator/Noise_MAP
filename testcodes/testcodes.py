import folium
import googlemaps
from googlemaps.convert import decode_polyline

# Initialize Google Maps client with your API key
api_key = "AIzaSyA1Kz-U4z5JTBOLDFGQQKAYTwZzPLaxF6E"  # Get it from https://console.cloud.google.com/
gmaps = googlemaps.Client(key=api_key)

# Define start and end locations
start_location = "Delhi, India"
end_location = "Noida, India"

# Request directions
directions = gmaps.directions(
    origin=start_location,
    destination=end_location,
    mode="driving",  # Options: 'driving', 'walking', 'bicycling', 'transit'
    alternatives = True
)

# Extract route geometry (polyline)
route_polyline = directions[0]['overview_polyline']['points']

# Decode the polyline into (latitude, longitude) pairs
route_coords = decode_polyline(route_polyline)
route_coords = [[d['lat'], d['lng']] for d in route_coords]
# print(route_coords)
# Create a Folium map
mymap = folium.Map(location=route_coords[0], zoom_start=12)

# Add route to the map
folium.PolyLine(locations=route_coords, color="green", weight=5, tooltip="Google Route").add_to(mymap)

# Add start and end markers
folium.Marker(location=route_coords[0], popup="Start: Delhi").add_to(mymap)
folium.Marker(location=route_coords[-1], popup="End: Noida").add_to(mymap)

# Save the map to an HTML file
mymap.save("google_route_map.html")
