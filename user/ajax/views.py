from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import JsonResponse
from ..models import CustomUser as User
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
