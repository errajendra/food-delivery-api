from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from random import randint
from django.conf import settings
from django.template.loader import render_to_string
from .models import (
    Wallet, CustomUser as User,
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
        otp = randint(100000, 999999)
        instance.otp = otp
        instance.save()
        email_context = {
            "message": f"Hii, {instance.name} please verify your account with entering otp: {otp}",
            "name": "Food Delivery Team",
            "email": f"{settings.DEFAULT_FROM_EMAIL}"
        }
        email_message = render_to_string(
            'user/email/created.html', email_context
        )
        email = EmailMessage(
            subject = "Veification Code- Food Delivery Subscription",
            body = email_message,
            to = [instance.email]
        )
        email.send(fail_silently=False)
