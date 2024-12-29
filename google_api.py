import numpy as np
import requests
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Replace with your actual Google Maps API Key
API_KEY = "AIzaSyA1Kz-U4z5JTBOLDFGQQKAYTwZzPLaxF6E"

# Example function to get place data from Google Maps API
def get_place_data(location, radius=5000):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&key={API_KEY}"
    response = requests.get(url)
    return response.json().get('results', [])

# Function to preprocess data
def preprocess_data(data):
    features = []
    labels = []
    
    for place in data:
        # Extract relevant features from the place data
        place_rating = place.get('rating', 0)  # Use 0 if rating is not available
        user_ratings_total = place.get('user_ratings_total', 0)  # Use 0 if not available
        place_types = len(place.get('types', []))  # Number of types the place belongs to
        
        # Example: Assign a label for sound likelihood (randomly in this case)
        sound_likelihood = 1 if place_rating > 3.5 else 0  # Placeholder logic
        
        features.append([place_rating, user_ratings_total, place_types])
        labels.append(sound_likelihood)

    return np.array(features), np.array(labels)

# Example of getting data from Google Maps API (replace with real data fetching)
location = '40.748817,-73.985428'  # Example: Latitude and Longitude of a place
data = get_place_data(location)

# Preprocess the data
features, labels = preprocess_data(data)

# Standardize the features
scaler = StandardScaler()
features = scaler.fit_transform(features)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Reshape data for CNN input (assuming 1D features)
X_train = X_train[..., np.newaxis]
X_test = X_test[..., np.newaxis]

# Adjust the input shape and kernel size to avoid negative output size
input_shape = (X_train.shape[1], 1)

kernel_size = min(input_shape[0], 3)

# Build the CNN model
model = Sequential([
    Conv1D(32, kernel_size=kernel_size, activation='relu', input_shape=input_shape),
    Conv1D(64, kernel_size=kernel_size, activation='relu'),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')  # Output is binary (sound likelihood)
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_accuracy}")

# Predict sound likelihood for new data
new_data = scaler.transform([[4.5, 150, 5]])  # Example new data with rating, user_ratings_total, place_types
new_data = new_data[..., np.newaxis]
prediction = model.predict(new_data)
print(f"Sound Likelihood: {prediction[0][0]}")
