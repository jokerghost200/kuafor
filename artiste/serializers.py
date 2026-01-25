from rest_framework import serializers
from .models import ArtisteProfile

class ArtisteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtisteProfile
        fields = ['id', 'nom_salon', 'description', 'latitude', 'longitude']  # + tout ce que tu veux renvoyer
