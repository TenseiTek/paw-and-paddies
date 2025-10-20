from django.shortcuts import render
from rest_framework import generics
from .models import PawProfile
from .serializers import PawProfileSerializer

class PawProfileList(generics.ListCreateAPIView):
    queryset = PawProfile.objects.all()
    serializer_class = PawProfileSerializer


# Create your views here.
