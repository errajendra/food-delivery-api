from django.core.validators import RegexValidator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect
import re


"""phone number validation"""
phone_regex_formate = r"^[6-9]\d{9}$"
phone_invalid_message = "Enter a 10 digit valid mobile number."

# Phone number validator
phone_validator = RegexValidator(
    regex = phone_regex_formate,
    message = phone_invalid_message,
)


"""pin or zip code validation"""
zip_regex_formate = r"^[1-9]\d{3,5}$"
zip_invalid_message = "Enter a 6 digit valid ZIP code."

# zip number validator
zip_validator = RegexValidator(
    regex = zip_regex_formate,
    message = zip_invalid_message,
)

name_validator = RegexValidator(
    regex = r"^[A-Z][a-zA-Z '.-]*[A-Za-z][^-]$",
    # message="Enter valid name."
    message="Name must start with capital letter and can contain only letters or spaces."
)

password_regx = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"

password_validator = RegexValidator(
    regex = password_regx,
    message = "Use a strong password"
)

def validate_password(password):
    # We use the re.match function to test the password against the pattern
    match = re.match(password_regx, password)
    # return True if the password matches the pattern, False otherwise
    return bool(match)

def encode_uid(pk):
    return force_str(urlsafe_base64_encode(force_bytes(pk)))


def decode_uid(pk):
    return force_str(urlsafe_base64_decode(pk))


def render_index_page(request):
    return redirect('index')
