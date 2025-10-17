from django.urls import path
from .views import create_dog_profile
from django.http import JsonResponse
from .views import create_dog_profile, test_bio
from .views import filter_dogs_by_trait
from . import views




urlpatterns = [
    #path('match/', match_dogs),  # ✅ This line adds the missing route
    path('create/', create_dog_profile),  # 👈 This matches /api/create/
    path('test/', lambda request: JsonResponse({'message': 'Routing works ✅'})),
    path('bio-test/', views.test_bio),  # 👈 New route for GPT bio
    path('filter/', views.filter_dogs_by_trait),
    path('ping/', lambda request: JsonResponse({'message': 'pong 🐾'})),
]
