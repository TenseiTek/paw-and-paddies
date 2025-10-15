from rest_framework import serializers
from .models import DogProfile

class DogProfileSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = DogProfile
        fields = ['id', 'name', 'breed', 'traits', 'latitude', 'longitude', 'bio', 'photo', 'photo_url']

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None
