from django.shortcuts import render
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import date
from .models import ArtisteProfile
from .serializers import ArtisteSerializer

@api_view(['GET'])
def rechercher_artistes(request):
    lat = request.query_params.get('lat')
    lng = request.query_params.get('lng')
    cat = request.query_params.get('category')

    user_loc = Point(float(lng), float(lat), srid=4326)

    # Filtrage selon la documentation [cite: 52, 53, 54, 55]
    artistes = ArtisteProfile.objects.filter(
        services__categorie=cat,
        is_active=True,
        date_expiration_abonnement__gte=date.today()
    ).annotate(
        distance=Distance('location', user_loc)
    ).order_by('distance')

    serializer = ArtisteSerializer(artistes, many=True)
    return Response(serializer.data)

def accueil(request):
    return render(request, 'accueil/index.html')