from .models import Place
from rest_framework import serializers


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id', 'place', 'adress', 'time', 'latitude', 'longitude', 'image_url')
