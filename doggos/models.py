from django.db import models


class DogProfile(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    traits = models.JSONField(default=list)
    latitude = models.FloatField()
    longitude = models.FloatField()
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='dog_photos/', blank=True, null=True) 

    def __str__(self):
        return self.name


