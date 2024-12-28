import json

with open("noise_routing_dataset.json") as f:
    s = f.read()
    noise_data = json.loads(s)

print(noise_data.keys())
# print(noise_data['routes'][1])
print(len(noise_data['noise'][0]))
print(noise_data['labels'][1])