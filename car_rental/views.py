from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Booking, Category
from .forms import BookingForm, ClientRegistrationForm 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from django.db.models import Q

def home(request):
    categories = Category.objects.all()
    featured_cars = Car.objects.filter(is_available=True).order_by('-id')[:6] 
    context = {'categories': categories, 'featured_cars': featured_cars}
    return render(request, 'car_rental/home.html', context)

def car_list(request):
    cars = Car.objects.filter(is_available=True)
    categories = Category.objects.all()
    brands = Car.objects.values_list('brand', flat=True).distinct()
    
    selected_category = request.GET.get('category')
    selected_brand = request.GET.get('brand')
    selected_transmission = request.GET.get('transmission')

    if selected_category:
        cars = cars.filter(category__name=selected_category)
    if selected_brand:
        cars = cars.filter(brand=selected_brand)
    if selected_transmission:
        cars = cars.filter(transmission=selected_transmission)

    context = {'cars': cars, 'categories': categories, 'brands': brands}
    return render(request, 'car_rental/car_list.html', context)

@login_required
def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    
    if request.method == 'POST':
        # On utilise le formulaire pour gérer proprement les dates (format ISO avec 'T')
        form = BookingForm(request.POST, car=car)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            booking.save() # Le prix est calculé par la méthode save() du modèle
            messages.success(request, f"Réservation confirmée pour la {car.brand} !")
            return redirect('my_bookings')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = BookingForm(car=car)

    return render(request, 'car_rental/car_detail.html', {'car': car, 'form': form})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'car_rental/my_bookings.html', {'bookings': bookings})

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    car = booking.car
    
    if request.method == 'POST':
        # On passe l'instance existante pour la mise à jour
        form = BookingForm(request.POST, instance=booking, car=car)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre réservation a été mise à jour.")
            return redirect('my_bookings')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = BookingForm(instance=booking, car=car)
    
    return render(request, 'car_rental/edit_booking.html', {'form': form, 'booking': booking, 'car': car})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status != 'Cancelled':
        booking.status = 'Cancelled'
        booking.save()
        messages.success(request, "Votre réservation a été annulée.")
    else:
        messages.error(request, "Cette réservation est déjà annulée.")
    return redirect('my_bookings')

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == 'Cancelled':
        booking.delete()
        messages.success(request, "Réservation supprimée de l'historique.")
    else:
        messages.error(request, "Seules les réservations annulées peuvent être supprimées.")
    return redirect('my_bookings')

def register(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé avec succès ! Connectez-vous.")
            return redirect('login')
    else:
        form = ClientRegistrationForm()
    return render(request, 'car_rental/register.html', {'form': form})

def about(request):
    return render(request, 'car_rental/about.html')