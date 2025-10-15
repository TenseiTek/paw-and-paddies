from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .serializers import DogProfileSerializer
from .geo_utils import find_nearby_dogs
from .models import DogProfile
from .ai_utils import generate_dog_bio, generate_fallback_bio
import json

@csrf_exempt
@api_view(['POST'])
def create_dog_profile(request):
    print("Raw traits from request:", request.data.get("traits"))

    data = request.data.copy()
    traits_raw = data.get("traits")

    # Accept either a raw list or a stringified JSON array
    if isinstance(traits_raw, list):
        data["traits"] = traits_raw
    elif isinstance(traits_raw, str):
        try:
            parsed = json.loads(traits_raw)
            if isinstance(parsed, list):
                data["traits"] = parsed
            else:
                return Response({"traits": ["Value must be a JSON array."]}, status=400)
        except json.JSONDecodeError:
            return Response({"traits": ["Value must be valid JSON."], "received": traits_raw}, status=400)
    else:
        return Response({"traits": ["Traits must be a list or JSON string."]})  # ✅ FIXED

    name = data.get("name")
    breed = data.get("breed")
    traits = data.get("traits")

    # ✅ GPT bio generation with fallback
    bio = generate_dog_bio(name, breed, traits)
    if not bio:
        bio = generate_fallback_bio(name, breed, traits)

    data["bio"] = bio

    # ✅ Use patched data (not request.data)
    serializer = DogProfileSerializer(data=data)
    if serializer.is_valid():
        new_dog = serializer.save()

        # ✅ Use the saved bio from serializer
        nearby_matches = find_nearby_dogs(
            lat=new_dog.latitude,
            lon=new_dog.longitude,
            exclude_id=new_dog.id
        )

        print("Returning response:", {
            "message": "Dog profile created!",
            "data": serializer.data,
            "bio": serializer.data.get("bio"),
            "nearby_matches": nearby_matches
        })

        return Response({
            "message": "Dog profile created!",
            "data": serializer.data,
            "bio": serializer.data.get("bio"),
            "nearby_matches": nearby_matches
        })
    else:
        print("Validation errors:", serializer.errors)
        return Response(serializer.errors, status=400)

@api_view(['GET'])
def test_bio(request):
    name = "Mochi"
    breed = "Shiba Inu"
    traits = ["loyal", "playful", "curious"]

    bio = generate_dog_bio(name, breed, traits)
    if not bio:
        bio = generate_fallback_bio(name, breed, traits)

    return Response({"bio": bio})

@api_view(['GET'])
def filter_dogs_by_trait(request):
    trait = request.GET.get("trait")
    if not trait:
        return Response({"error": "Trait is required"}, status=400)

    matching_dogs = DogProfile.objects.filter(traits__contains=[trait])
    results = [
        {
            "name": dog.name,
            "breed": dog.breed,
            "traits": dog.traits,
            "bio": dog.bio,
            "photo_url": dog.photo.url if dog.photo else None
        }
        for dog in matching_dogs
    ]
    return Response({"matches": results})



