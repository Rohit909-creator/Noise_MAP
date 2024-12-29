import folium

# Create a map centered around a location
m = folium.Map(location=[28.7041, 77.1025], zoom_start=12)

# Define a marker with a popup
popup_content = "This is Delhi, India! Noise Level: 75 dB"
marker = folium.Marker(
    location=[28.7041, 77.1025],
    popup=popup_content
).add_to(m)

# Add JavaScript to automatically open the popup on map load
m.get_root().html.add_child(folium.Element("""
    <script>
        // Automatically open the popup when the map loads
        document.addEventListener('DOMContentLoaded', function() {
            var marker = document.querySelector('.leaflet-marker-icon');
            if (marker) {
                marker.click();  // Simulate a click to open the popup
            }
        });
    </script>
"""))

# Save the map to an HTML file
m.save("auto_popup_map.html")
