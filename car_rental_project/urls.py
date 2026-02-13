from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from car_rental import views 

urlpatterns = [
    # --- ADMIN ---
    path('admin/', admin.site.urls),

    # --- PAGES ---
    path('', views.home, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('about/', views.about, name='about'),
    path('booking/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('booking/edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    
    # --- LA LIGNE MANQUANTE ICI ---
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    # --- AUTH ---
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='car_rental/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)