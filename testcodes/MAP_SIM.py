import folium
import random

# Function to generate random noise data points
def generate_noise_data(center_lat, center_lng, count):
    noise_data = []
    for _ in range(count):
        # Generate random lat/lng near the center point
        random_lat = center_lat + (random.uniform(-0.05, 0.05))
        random_lng = center_lng + (random.uniform(-0.05, 0.05))
        random_noise = random.randint(40, 100)  # Noise levels in dB (40-100)
        noise_data.append((random_lat, random_lng, random_noise))
    return noise_data

# Initialize map centered at a specific location
center_lat = 8.484140536292756  # Example: Delhi, India
center_lng = 76.94341420944959  # Example: Delhi, India
noise_map = folium.Map(location=[center_lat, center_lng], zoom_start=12)

# Generate 50 random noise data points
noise_data = generate_noise_data(center_lat, center_lng, count=50)

# Add noise points to the map as markers with color-coded noise levels
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
    ).add_to(noise_map)

# Save the map to an HTML file
noise_map.save("simulated_noise_map.html")

print("Noise map generated! Open 'simulated_noise_map.html' to view it.")
