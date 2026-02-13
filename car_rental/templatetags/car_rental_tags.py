from django import template
from car_rental.models import Booking, Car
from django.db.models import Sum
from django.utils import timezone

register = template.Library()

@register.simple_tag
def get_total_revenue():
    # On calcule le revenu sur tout ce qui est payé, en cours ou terminé
    total = Booking.objects.filter(
        status__in=['Confirmed', 'Active', 'Completed']
    ).aggregate(Sum('total_price'))['total_price__sum']
    return total or 0

@register.simple_tag
def get_active_rentals():
    return Booking.objects.filter(status='Active').count()

@register.simple_tag
def get_overdue_rentals():
    
    return Booking.objects.filter(
        status='Active', 
        end_date__lt=timezone.now().date()
    ).count()

@register.simple_tag
def get_total_cars():
    return Car.objects.count()