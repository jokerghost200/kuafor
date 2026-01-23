from rest_framework import serializers
from .models import ArtisteProfile, Service

class ArtisteSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()
    photo_principale = serializers.SerializerMethodField()

    class Meta:
        model = ArtisteProfile
        fields = ['id', 'nom_salon', 'description', 'distance', 'photo_principale']

    def get_distance(self, obj):
        # On récupère la distance calculée par la vue (annotate)
        if hasattr(obj, 'distance'):
            return round(obj.distance.km, 2)
        return None

    def get_photo_principale(self, obj):
        # Récupère la première image du portfolio [cite: 27]
        photo = obj.portfolio.first()
        return photo.image.url if photo else None