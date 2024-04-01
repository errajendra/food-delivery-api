from random import randint
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage


def send_otp(user):
    otp = randint(100000, 999999)
    user.otp = otp
    user.save()
    email_context = {
        "otp": otp,
        "email": f"contact@atmkaro.in"
    }
    email_message = render_to_string(
        'user/email/otp.html', email_context
    )
    if user.email:
        email = EmailMessage(
            subject = "Your login OTP is ready to unlock a world of flavor at Amritsari Tadke Mein! 🍲",
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
    # To be removed in production
    print("OTP Verification Failed")
    if user.email in ["ankitp@wooshelf.com", "rajendras@wooshelf.com"] and int(otp) == 123456:
        return True
    if int(user.mobile_number[4:]) == int(otp):
        return True
    # OTP Verification failed
    return False
