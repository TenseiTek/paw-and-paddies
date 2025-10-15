import requests

url = "http://127.0.0.1:8001/api/create/"
data = {
    "name": "Charlie",
    "breed": "Corgi",
    "traits": ["funny", "loyal"],
    "latitude": 48.8570,
    "longitude": 2.3510
}

response = requests.post(url, json=data)
print("✅ Status Code:", response.status_code)
print("📦 Response JSON:", response.json())
