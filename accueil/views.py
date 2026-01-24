from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import date
from .models import ArtisteProfile, Service
from .serializers import ArtisteSerializer
from .utils import haversine_distance
from django.shortcuts import render, redirect



@api_view(['GET'])
def rechercher_artistes(request):
    lat = request.query_params.get('lat')
    lng = request.query_params.get('lng')
    cat = request.query_params.get('category')

    if not lat or not lng or not cat:
        return Response(
            {"error": "lat, lng et category sont requis"},
            status=400
        )

    try:
        user_lat = float(lat)
        user_lng = float(lng)
    except ValueError:
        return Response({"error": "Coordonnées invalides"}, status=400)

    if cat not in Service.Categories.values:
        return Response({"error": "Catégorie invalide"}, status=400)

    artistes = ArtisteProfile.objects.filter(
        services__categorie=cat,
        is_active=True,
        date_expiration_abonnement__gte=date.today(),
        latitude__isnull=False,
        longitude__isnull=False
    ).distinct()

    # Calcul de distance en Python
    results = []
    for artiste in artistes:
        distance = haversine_distance(
            user_lat,
            user_lng,
            artiste.latitude,
            artiste.longitude
        )
        artiste.distance = round(distance, 2)
        results.append(artiste)

    # Trier par distance
    results.sort(key=lambda x: x.distance)

    serializer = ArtisteSerializer(results, many=True)
    return Response(serializer.data)


def accueil(request):
    return render(request, 'accueil/index.html')
