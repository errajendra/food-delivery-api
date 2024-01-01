import razorpay
from django.conf import settings

MURCHENT_ID = settings.RAZOR_PAY_MURCHENT_ID
RAZOR_PAY_API_KEY = settings.RAZOR_PAY_API_KEY
RAZOR_PAY_API_SECRET = settings.RAZOR_PAY_API_SECRET
RAZOR_PAY_APP_TITLE = settings.RAZOR_PAY_APP_TITLE
APP_VERSION = "1.0"
client = razorpay.Client(auth=(RAZOR_PAY_API_KEY, RAZOR_PAY_API_SECRET))
client.set_app_details({"title" : RAZOR_PAY_APP_TITLE, "version" : APP_VERSION})
