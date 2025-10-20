from rest_framework import serializers
from .models import PawProfile

class PawProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PawProfile
        fields = '__all__'

