import folium
import googlemaps
from googlemaps.convert import decode_polyline
import random
import webbrowser
class Map:

    def __init__(self, start_location = "Delhi, India", end_location = "Old Delhi, India", probs=0.5):
        api_key = "AIzaSyA1Kz-U4z5JTBOLDFGQQKAYTwZzPLaxF6E"  # Get it from https://console.cloud.google.com/
        self.gmaps = googlemaps.Client(key=api_key)
        self.start_location = start_location
        self.end_location = end_location
        self.directions = None
        self.probs = probs

    def render_route(self):
        if self.directions == None:
            print("route function not called")
            return
        start_lat = self.directions[0]['legs'][0]['start_location']['lat']
        start_lng = self.directions[0]['legs'][0]['start_location']['lng']
        end_lat = self.directions[0]['legs'][0]['end_location']['lat']
        end_lng = self.directions[0]['legs'][0]['end_location']['lng']
        mymap = folium.Map(location=[start_lat, start_lng], zoom_start=12)
        colors = ["blue", "green", "purple", "orange", "red"]  # Different colors for different routes
        for idx, route in enumerate(self.directions):
            # Extract the route geometry (polyline)
            route_polyline = route['overview_polyline']['points']
            
            # Decode the polyline into (latitude, longitude) pairs
            route_coords = decode_polyline(route_polyline)
            route_coords = [[d['lat'], d['lng']] for d in route_coords]
            # Add the route to the map with a unique color

            noises = self.generate_noises(len(route_coords))
            for coords, noise in zip(route_coords, noises):
                # print(coords, noise)
                if random.uniform(0, 1) > self.probs:
                    lat, lng, noise = coords[0], coords[1], noise

                    # for lat, lng, noise_level in noise_data:
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
                color=colors[idx % len(colors)],  # Cycle through colors if more routes exist
                weight=5,
                tooltip=f"Route {idx + 1}"
            ).add_to(mymap)

        # Add start and end markers
        
        folium.Marker(location=[start_lat, start_lng], popup="Start: Delhi").add_to(mymap)
        folium.Marker(location=[end_lat, end_lng], popup="End: Old Delhi").add_to(mymap)
        # Save the map to an HTML file
        mymap.save("google_multiple_routes_map.html")
        file_path = "index.html"
        webbrowser.open(file_path)

    def show(self):
        pass


    def get_routes(self):
        # Request directions with alternatives enabled
        self.directions = self.gmaps.directions(
            origin=self.start_location,
            destination=self.end_location,
            mode="driving",  # Options: 'driving', 'walking', 'bicycling', 'transit'
            alternatives=True  # Request multiple routes
        )

    def generate_noises(self, count):
        noise_data = []
        for _ in range(count):
            random_noise = random.randint(40, 100)  # Noise levels in dB (40-100)
            noise_data.append(random_noise)
        return noise_data



if __name__ == "__main__":

    mapp = Map()
    # mapp.start_location
    # mapp.end_location
    mapp.get_routes()
    mapp.render_route()
