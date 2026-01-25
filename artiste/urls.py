from django.conf import settings
from django.conf.urls.static import static 
from . import views
from django.urls import path 

app_name = 'artiste'

urlpatterns = [
path('recherche/', views.rechercher_artistes, name='rechercher_artistes'),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)