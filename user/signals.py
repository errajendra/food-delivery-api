from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from random import randint
from django.conf import settings
from django.template.loader import render_to_string
from .models import (
    CustomUser as User,
    NotificationSetting,
)


""" This will create notification and send otp on his mail. """
@receiver(post_save, sender=User)
def create_notification_setting(sender, instance, created, **kwargs):
    if created:
        NotificationSetting.objects.create(
            user = instance
        )
        # Sending otp on his mail
        if instance.email:
            otp = randint(100000, 999999)
            instance.otp = otp
            instance.save()
            email_context = {
                "otp": otp,
                "name": "The Amritsari Tadke Mein Team",
                "email": f"contact@atmkaro.in"
            }
            email_message = render_to_string(
                'user/email/created.html', email_context
            )
            email = EmailMessage(
                subject = "Welcome to Amritsari Tadke Mein! Your Flavorful Journey Starts Here! 🌟",
                body = email_message,
                to = [instance.email]
            )
            email.send(fail_silently=False)
