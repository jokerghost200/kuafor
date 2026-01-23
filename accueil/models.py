from django.db import models

# Create your models here.
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class ArtisteProfile(models.Model):
    # Liaison avec l'utilisateur (Authentification via numéro de téléphone) [cite: 11]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom_salon = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Matching Géospatial [cite: 50, 51]
    location = models.PointField(geography=True, srid=4326, blank=True, null=True)
    
    # Contrôle de Visibilité (Phase 3) [cite: 66, 67]
    is_active = models.BooleanField(default=False)
    
    # Gestion d'abonnement (Business Model) [cite: 30, 40]
    date_inscription = models.DateField(auto_now_add=True)
    date_expiration_abonnement = models.DateField(null=True, blank=True)

    @property
    def est_visible(self):
        """Vérifie les 3 conditions : Actif, Abonnement valide, Localisation présente [cite: 52, 53, 54, 55]"""
        return (
            self.is_active and 
            self.date_expiration_abonnement and 
            self.date_expiration_abonnement >= timezone.now().date() and
            self.location is not None
        )

    def __str__(self):
        return self.nom_salon

class Service(models.Model):
    CATEGORIES = [
        ('COIFFURE_H', 'Coiffure Homme'), [cite: 20]
        ('COIFFURE_F', 'Coiffure Femme'), [cite: 21]
        ('MAKEUP', 'Make-up professionnel'), [cite: 22]
        ('ONGLERIE', 'Onglerie'), [cite: 23]
    ]
    
    artiste = models.ForeignKey(ArtisteProfile, related_name='services', on_delete=models.CASCADE)
    categorie = models.CharField(max_length=20, choices=CATEGORIES)
    nom_prestation = models.CharField(max_length=100) # ex: "Pose de gel" [cite: 26]
    prix = models.DecimalField(max_digits=10, decimal_places=0) # En XAF [cite: 42]
    duree_estimee = models.IntegerField(help_text="Durée en minutes", default=30)

    def __str__(self):
        return f"{self.nom_prestation} ({self.artiste.nom_salon})"

class PortfolioImage(models.Model):
    """Portfolio des réalisations de l'artiste [cite: 27, 60]"""
    artiste = models.ForeignKey(ArtisteProfile, related_name='portfolio', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='portfolio/')