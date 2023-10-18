from rest_framework.exceptions import APIException


class InvaliedToken(APIException):
    status_code = 400
    default_detail = {
        'status': 400,
        'message': "Invalid token"
    }
    default_code = 'invalid_token'
