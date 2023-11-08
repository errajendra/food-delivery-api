from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import JsonResponse
from ..models import CustomUser as User
from meal.models import PlanPurchase, MealRequestDaily
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime



def update_user_active(request):
    user_id = request.POST.get('user_id')
    new_status = int(request.POST.get('new_status'))
    try:
        user = User.objects.get(pk=user_id)
        user.is_active = bool(new_status)
        user.save()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})

def update_plan_purchase_active(request):
    plan_id = request.POST.get('plan_id')
    print(plan_id)
    new_status = int(request.POST.get('new_status'))
    try:
        plan = PlanPurchase.objects.get(pk=plan_id)
        plan.status = bool(new_status)
        plan.save()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Plan not found'})
    
    
def update_meal_active_ajax(request):
    meal_id = request.POST.get('meal_id')
    new_status = request.POST.get('new_status')
    try:
        meal = MealRequestDaily.objects.get(pk=meal_id)
        meal.status = new_status
        meal.save()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Meal not found'})
        