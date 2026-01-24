from django.conf import settings
from django.conf.urls.static import static 
from . import views
from django.urls import path 

app_name = 'accueil'

urlpatterns = [
    # La page d'accueil (votre interface orange et blanche)
    path('', views.accueil, name='accueil'),
    
    # La route API pour le bouton "Localiser"
    path('api/recherche/', views.rechercher_artistes, name='api-recherche'),
]

# Gestion des médias (indispensable pour les portfolios d'artistes)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)