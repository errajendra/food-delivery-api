from random import randint
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
import requests


# Sending otp to user
def send_otp(user):
    otp = randint(100000, 999999)
    user.otp = otp
    user.save()
    
    otp_sent = False
    
    # Send Code On WhatsApp 
    print(user.mobile_number)
    if user.mobile_number:
        url = "https://api.versal.one/f8fea0d3-2c4c-478b-99e8-c9f88383d71f"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer c9f88383d71f"
        }
        row = {
            "purpose":"sendotp",
            "otp": f"{otp}",
            "to": f"91{user.mobile_number}"
        }

        response = requests.post(url, headers=headers, json=row)
        # print(response.json())
        if response.status_code == 200:
            otp_sent = True
    
    # Send Oztp on Email
    if user.email:
        email_context = {
            "otp": otp,
            "email": f"contact@atmkaro.in"
        }
        email_message = render_to_string(
            'user/email/otp.html', email_context
        )
        email = EmailMessage(
            subject = "Your login OTP is ready to unlock a world of flavor at Amritsari Tadke Mein! 🍲",
            body = email_message,
            to = [user.email]
        )
        email.send(fail_silently=False)
        otp_sent = True
        
    return otp_sent


# Verify Otp method
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
