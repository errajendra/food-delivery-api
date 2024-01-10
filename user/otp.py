from random import randint
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage


def send_otp(user):
    otp = randint(100000, 999999)
    user.otp = otp
    user.save()
    email_context = {
        "message": f"Hii, {user.name} please verify your account with entering otp: {otp}",
        "name": "Food Delivery (ATM)",
        "email": f"{settings.DEFAULT_FROM_EMAIL}"
    }
    email_message = render_to_string(
        'user/email/created.html', email_context
    )
    if user.email:
        email = EmailMessage(
            subject = "Food Delivery (ATM): OTP",
            body = email_message,
            to = [user.email]
        )
        email.send(fail_silently=False)
    return True


def verify_otp(user, otp):
    try:
        otp_int = int(otp)
        if otp_int == int(user.otp):
            return True
    except:
        pass
    return False


