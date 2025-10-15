from math import radians, cos, sin, asin, sqrt
from .models import DogProfile

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def find_nearby_dogs(lat, lon, exclude_id=None, radius_km=5):
    nearby = []
    for dog in DogProfile.objects.exclude(id=exclude_id):
        distance = haversine(lat, lon, dog.latitude, dog.longitude)
        if distance <= radius_km:
            nearby.append({
                "name": dog.name,
                "breed": dog.breed,
                "traits": dog.traits,
                "distance_km": round(distance, 2)
            })
    return nearby
