from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator


class ArtisteProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    nom_salon = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    is_active = models.BooleanField(default=False)

    date_inscription = models.DateField(auto_now_add=True)
    date_expiration_abonnement = models.DateField(null=True, blank=True)

    @property
    def est_visible(self):
        today = timezone.now().date()
    
    # Si l'une des conditions nécessaires est manquante, on retourne False
        if not self.is_active:
            return False
        if self.latitude is None or self.longitude is None:
                return False
        if self.date_expiration_abonnement is None:
                return False
    
    # Comparaison sûre, on sait que date_expiration_abonnement n'est pas None
        return self.date_expiration_abonnement >= today

    def __str__(self):
        return self.nom_salon

    class Meta:
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['date_expiration_abonnement']),
        ]


class Service(models.Model):
    class Categories(models.TextChoices):
        COIFFURE_H = 'COIFFURE_H', 'Coiffure Homme'
        COIFFURE_F = 'COIFFURE_F', 'Coiffure Femme'
        MAKEUP = 'MAKEUP', 'Make-up professionnel'
        ONGLERIE = 'ONGLERIE', 'Onglerie'

    artiste = models.ForeignKey(
        ArtisteProfile,
        related_name='services',
        on_delete=models.CASCADE
    )
    categorie = models.CharField(
        max_length=20,
        choices=Categories.choices
    )
    nom_prestation = models.CharField(max_length=100)
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        validators=[MinValueValidator(0)]
    )
    duree_estimee = models.PositiveIntegerField(default=30)

    def __str__(self):
        return f"{self.nom_prestation} ({self.artiste.nom_salon})"


class PortfolioImage(models.Model):
    artiste = models.ForeignKey(
        ArtisteProfile,
        related_name='portfolio',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='portfolio/')

    def __str__(self):
        return f"Portfolio - {self.artiste.nom_salon}"