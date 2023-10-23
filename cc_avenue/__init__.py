
from django.conf import settings

WORKING_KEY = settings.CC_A_WORKING_KEY
ACCESS_CODE = settings.CC_A_ACCESS_CODE
MERCHANT_CODE = settings.CC_A_MERCHANT_ID
CURRENCY = settings.CC_A_CURRENCY

REDIRECT_URL = "/payment/check/"
CANCEL_URL = "/payment/cancel/"
CC_PAY_MODE = "test" # test or secure

# ccavenue = CCAvenue(WORKING_KEY, ACCESS_CODE, MERCHANT_CODE, REDIRECT_URL, CANCEL_URL)
