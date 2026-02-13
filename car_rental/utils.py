import os
from io import BytesIO
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from xhtml2pdf import pisa
from django.conf import settings

def generer_et_envoyer_confirmation(booking):
    # Sécurité : Vérifier si l'utilisateur a une adresse email
    if not booking.user.email:
        print(f"Erreur : L'utilisateur {booking.user.username} n'a pas d'adresse email.")
        return False

    # 1. Préparation des données pour le PDF
    context = {
        'booking': booking,
        'today': timezone.now(),
    }
    
    # 2. Rendu du template HTML
    html_string = render_to_string('car_rental/contrat_pdf.html', context)
    
    # 3. Création du PDF en mémoire
    result = BytesIO()
    # On spécifie l'encodage UTF-8 pour supporter les caractères spéciaux (accents, DT)
    pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
    
    if not pdf.err:
        pdf_content = result.getvalue()
        
        # 4. Préparation de l'Email avec détails horaires
        start_dt = booking.start_date.strftime("%d/%m/%Y à %H:%M")
        end_dt = booking.end_date.strftime("%d/%m/%Y à %H:%M")
        
        subject = f"✅ Confirmation de Réservation #{booking.id} - BossCar Location"
        
        message = (
            f"Bonjour {booking.user.username},\n\n"
            f"Votre réservation pour le véhicule {booking.car.brand} {booking.car.model} est confirmée.\n\n"
            f"📅 Période de location :\n"
            f"   - Départ : {start_dt}\n"
            f"   - Retour : {end_dt}\n\n"
            f"Vous trouverez ci-joint votre contrat de location à présenter lors du retrait du véhicule.\n\n"
            f"Merci de votre confiance !\n\n"
            f"L'équipe DriveRent."
        )
        
        email = EmailMessage(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
            [booking.user.email],
        )
        
        # 5. Attachement du fichier
        filename = f'Contrat_BossCar_{booking.id}.pdf'
        email.attach(filename, pdf_content, 'application/pdf')
        
        try:
            email.send()
            return True
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email : {e}")
            return False
            
    return False