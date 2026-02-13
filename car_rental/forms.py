from django import forms
from .models import Booking
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        # Ajout de 'payment_method' dans les champs du formulaire
        fields = ['start_date', 'end_date', 'payment_method']
        widgets = {
            'start_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}, 
                format='%Y-%m-%dT%H:%M'
            ),
            'end_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}, 
                format='%Y-%m-%dT%H:%M'
            ),
            # Widget pour le choix du mode de paiement
            'payment_method': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.car = kwargs.pop('car', None)
        super(BookingForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and self.car:
            if start_date < timezone.now():
                raise forms.ValidationError("La date et l'heure de début ne peuvent pas être dans le passé.")
            
            if end_date <= start_date:
                raise forms.ValidationError("La date de retour doit être strictement après la date de départ.")

            overlapping_bookings = Booking.objects.filter(
                car=self.car,
                status__in=['Confirmed', 'Active']
            ).filter(
                Q(start_date__lt=end_date, end_date__gt=start_date)
            )

            # On exclut la réservation actuelle si on est en train de la modifier
            if self.instance.pk:
                overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)

            if overlapping_bookings.exists():
                raise forms.ValidationError("⚠️ Ce véhicule est déjà réservé sur ce créneau horaire.")
        
        return cleaned_data

class ClientRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'votre@email.com'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email