from rest_framework import serializers
from .models import ArtisteProfile


class ArtisteSerializer(serializers.ModelSerializer):
    distance = serializers.FloatField(read_only=True)

    class Meta:
        model = ArtisteProfile
        fields = [
            'id',
            'nom_salon',
            'description',
            'latitude',
            'longitude',
            'distance'
        ]
