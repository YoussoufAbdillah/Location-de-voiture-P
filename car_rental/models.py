from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import math

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.name

class Car(models.Model):
    TRANSMISSION_CHOICES = [('Manual', 'Manuelle'), ('Automatic', 'Automatique')]
    FUEL_CHOICES = [('Gasoline', 'Essence'), ('Diesel', 'Diesel'), ('Electric', 'Électrique')]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Catégorie")
    brand = models.CharField(max_length=100, verbose_name="Marque")
    model = models.CharField(max_length=100, verbose_name="Modèle")
    image = models.ImageField(upload_to='cars/')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix/Jour")
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, verbose_name="Transmission")
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, verbose_name="Carburant")
    
    seats = models.PositiveIntegerField(default=5, verbose_name="Nombre de places")
    doors = models.PositiveIntegerField(default=5, verbose_name="Nombre de portes")
    
    is_available = models.BooleanField(default=True, verbose_name="Disponible")

    class Meta:
        verbose_name = "Voiture"
        verbose_name_plural = "Voitures"

    def __str__(self):
        return f"{self.brand} {self.model}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'En attente'),
        ('Confirmed', 'Confirmé'),
        ('Active', 'Véhicule en circulation'),
        ('Completed', 'Véhicule rendu'),
        ('Cancelled', 'Annulé'),
    ]

    PAYMENT_CHOICES = [
        ('Card', 'Carte Bancaire'),
        ('Agency', 'Paiement à l\'agence'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Client")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Voiture")
    
    start_date = models.DateTimeField(verbose_name="Date et Heure de départ")
    end_date = models.DateTimeField(verbose_name="Date et Heure de retour")
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, verbose_name="Prix Total")
    
    # NOUVEAU CHAMP : Mode de paiement
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_CHOICES, 
        default='Agency', 
        verbose_name="Mode de paiement"
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending', verbose_name="Statut")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"

    @property
    def is_overdue(self):
        return self.status == 'Active' and self.end_date < timezone.now()

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            total_seconds = delta.total_seconds()
            days = math.ceil(total_seconds / (24 * 3600))
            
            if days <= 0:
                days = 1
                
            self.total_price = days * self.car.price_per_day
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Réservation {self.id} - {self.user.username} ({self.status})"