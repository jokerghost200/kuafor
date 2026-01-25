from django.contrib import admin
from .models import ArtisteProfile, Service, PortfolioImage

# --- Admin pour ArtisteProfile ---
@admin.register(ArtisteProfile)
class ArtisteProfileAdmin(admin.ModelAdmin):
    list_display = (
        'nom_salon',
        'user',
        'is_active',
        'date_inscription',
        'date_expiration_abonnement',
        'est_visible',
    )
    list_filter = ('is_active',)
    search_fields = ('nom_salon', 'user__username')
    readonly_fields = ('est_visible', 'date_inscription')

# --- Admin pour Service ---
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nom_prestation', 'artiste', 'categorie', 'prix', 'duree_estimee')
    list_filter = ('categorie',)
    search_fields = ('nom_prestation', 'artiste__nom_salon')

# --- Admin pour PortfolioImage ---
@admin.register(PortfolioImage)
class PortfolioImageAdmin(admin.ModelAdmin):
    list_display = ('artiste', 'image')
    search_fields = ('artiste__nom_salon',)
