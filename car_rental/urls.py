from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('register/', views.register, name='register'),
    path('my-bookings/', views.my_bookings, name='my_bookings'), 
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('booking/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('booking/edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),

]