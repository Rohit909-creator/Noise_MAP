import folium
import googlemaps
from googlemaps.convert import decode_polyline
import random
import requests

class Map:

    def __init__(self, start_location="Delhi, India", end_location="Old Delhi, India", probs=0.5):
        self.api_key = "AIzaSyA1Kz-U4z5JTBOLDFGQQKAYTwZzPLaxF6E"  # Get it from https://console.cloud.google.com/
        self.gmaps = googlemaps.Client(key=self.api_key)
        self.start_location = start_location
        self.end_location = end_location
        self.directions = None
        self.probs = probs

    def render_route(self):
        if self.directions is None:
            print("route function not called")
            return

        start_lat = self.directions[0]['legs'][0]['start_location']['lat']
        start_lng = self.directions[0]['legs'][0]['start_location']['lng']
        end_lat = self.directions[0]['legs'][0]['end_location']['lat']
        end_lng = self.directions[0]['legs'][0]['end_location']['lng']

        mymap = folium.Map(location=[start_lat, start_lng], zoom_start=12)
        colors = ["blue", "green", "purple", "orange", "red"]  # Different colors for different routes

        for idx, route in enumerate(self.directions):
            route_polyline = route['overview_polyline']['points']
            route_coords = decode_polyline(route_polyline)
            route_coords = [[d['lat'], d['lng']] for d in route_coords]

            noises = self.generate_noises(len(route_coords))
            for coords, noise in zip(route_coords, noises):
                if random.uniform(0, 1) > self.probs:
                    lat, lng, noise = coords[0], coords[1], noise

                    if noise <= 60:
                        color = 'green'  # Low noise
                    elif 60 < noise <= 80:
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
                        popup=f"Noise Level: {noise} dB"
                    ).add_to(mymap)

            folium.PolyLine(
                locations=route_coords,
                color=colors[idx % len(colors)],
                weight=5,
                tooltip=f"Route {idx + 1}"
            ).add_to(mymap)

        # Add start and end markers
        folium.Marker(location=[start_lat, start_lng], popup=f"Start: {self.start_location}").add_to(mymap)
        folium.Marker(location=[end_lat, end_lng], popup=f"End: {self.end_location}").add_to(mymap)

        # Add event markers
        events = self.extract_events(start_lat, start_lng)
        for event_name, event_data in events.items():
            folium.Marker(
                location=[event_data['latitude'], event_data['longitude']],
                popup=f"{event_name}<br>Address: {event_data['address']}<br>Rating: {event_data['rating']}",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(mymap)

        mymap.save("./templates/noise_map.html")

    def get_routes(self):
        self.directions = self.gmaps.directions(
            origin=self.start_location,
            destination=self.end_location,
            mode="driving",
            alternatives=True
        )

    def generate_noises(self, count):
        return [random.randint(40, 100) for _ in range(count)]

    def extract_events(self, lat, lng):
        radius = 5000  # Search radius in meters
        keyword = "event hall|auditorium|grounds"
        url = (f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
               f"location={lat},{lng}&radius={radius}&keyword={keyword}&key={self.api_key}")

        response = requests.get(url)
        data = response.json()

        needed_data = {}
        if "results" in data:
            for place in data["results"]:
                name = place.get("name")
                address = place.get("vicinity")
                rating = place.get("rating", "No rating")
                latitude = place["geometry"]["location"]["lat"]
                longitude = place["geometry"]["location"]["lng"]

                needed_data[name] = {
                    "address": address,
                    "rating": rating,
                    "latitude": latitude,
                    "longitude": longitude
                }

        return needed_data

if __name__ == "__main__":
    mapp = Map()
    mapp.get_routes()
    mapp.render_route()
