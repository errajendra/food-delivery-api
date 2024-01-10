from rest_framework.exceptions import APIException


class NoRemainMealsAvlSubscription(APIException):
    status_code = 400
    default_detail = {
        'status': 400,
        'message': "No remaining meals on this purchase subscription.",
        'errors': []
    }
    default_code = 'no_remaining_meals_for_purchage_plan'



""" Exception for PlanPurchaseDoesNotExist. """
class PlanPurchaseDoesNotExist(APIException):
    status_code = 400
    default_detail = {
        "status": 400,
        "message": "Invalid plan purchase ID",
        "errors": {"plan_purchese_id": ["Invalid plan purchase ID."]}
    }



""" Exception for MealDoesNotExist. """
class MealDoesNotExist(APIException):
    status_code = 400
    default_detail = {
        "status": 400,
        "message": "BAD REQUEST",
        "errors": {"meal_id": ["Invalid meal ID."]}
    }