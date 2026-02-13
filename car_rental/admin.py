from django.contrib import admin, messages
from django.utils.html import format_html
from .models import Car, Category, Booking
from django.db.models import Sum
from django.utils import timezone
from .utils import generer_et_envoyer_confirmation 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# --- PERSONNALISATION DE L'ADMIN UTILISATEUR ---
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

# --- CONFIGURATION DE L'INTERFACE ---
admin.site.site_header = "DriveRent Admin"
admin.site.site_title = "Gestion de Location"
admin.site.index_title = "Tableau de Bord de l'Agence"

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('display_image', 'brand', 'model', 'category', 'seats', 'doors', 'fuel_type', 'price_per_day', 'is_available')
    list_filter = ('category', 'transmission', 'fuel_type', 'seats', 'is_available')
    search_fields = ('brand', 'model')
    list_editable = ('is_available', 'price_per_day', 'seats', 'doors')

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height:auto; border-radius:5px;" />', obj.image.url)
        return "Pas d'image"
    display_image.short_description = 'Aperçu'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # Ajout de 'payment_method' dans la liste d'affichage
    list_display = ('id', 'user', 'car', 'display_start', 'display_end', 'payment_method', 'total_price', 'colored_status')
    # Ajout de 'payment_method' dans les filtres à droite
    list_filter = ('status', 'payment_method', 'start_date', 'car')
    search_fields = ('user__username', 'car__brand')
    
    actions = ['make_Confirm_with_notif', 'make_started', 'make_returned', 'make_cancelled']

    # --- FORMATAGE DATE & HEURE ---
    def display_start(self, obj):
        return obj.start_date.strftime("%d/%m/%Y %H:%M")
    display_start.short_description = "Départ (Heure)"

    def display_end(self, obj):
        return obj.end_date.strftime("%d/%m/%Y %H:%M")
    display_end.short_description = "Retour (Heure)"

    # --- ACTIONS ---
    @admin.action(description="✅ Confirmer et Notifier (Email PDF)")
    def make_Confirm_with_notif(self, request, queryset):
        count = 0
        for booking in queryset:
            booking.status = 'Confirmed'
            booking.save()
            if generer_et_envoyer_confirmation(booking):
                count += 1
            else:
                self.message_user(request, f"⚠️ Erreur d'envoi mail pour {booking.user.username}", level=messages.ERROR)
        self.message_user(request, f"✅ {count} réservation(s) confirmée(s) et notifiée(s).", level=messages.SUCCESS)

    @admin.action(description="🚗 Confirmer le DÉPART")
    def make_started(self, request, queryset):
        queryset.update(status='Active')
        self.message_user(request, "Le véhicule est maintenant en circulation.")

    @admin.action(description="🏁 Confirmer le RETOUR")
    def make_returned(self, request, queryset):
        queryset.update(status='Completed')
        self.message_user(request, "Les véhicules sont marqués comme rendus.")

    @admin.action(description="❌ Annuler la réservation")
    def make_cancelled(self, request, queryset):
        queryset.update(status='Cancelled')

    # --- STYLE DU STATUT (Badge de couleur) ---
    def colored_status(self, obj):
        colors = {
            'Confirmed': '#28a745', 
            'Active': '#007bff',    
            'Completed': '#6c757d', 
            'Cancelled': '#dc3545', 
            'Pending': '#ffc107',   
        }
        color = colors.get(obj.status, '#333')
        label = obj.get_status_display()
        
        if obj.status == 'Active' and obj.end_date < timezone.now():
            color = '#d63031'
            label = "🚨 EN RETARD"
            
        return format_html(
            '<b style="color:white; background:{}; padding:5px 12px; border-radius:15px; font-size:10px; display:inline-block; min-width:95px; text-align:center;">{}</b>',
            color, label
        )
    colored_status.short_description = 'Statut'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        extra_context = extra_context or {}
        total = qs.filter(status__in=['Confirmed', 'Active', 'Completed']).aggregate(Sum('total_price'))['total_price__sum']
        extra_context['total_revenue'] = total if total else 0
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Category)