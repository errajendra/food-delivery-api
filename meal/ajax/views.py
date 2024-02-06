from django.http.response import JsonResponse
from meal.models import CustomerSupport
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime



def update_help_active(request):
    help_id = request.POST.get('help_id')
    new_status = request.POST.get('new_status')
    try:
        help = CustomerSupport.objects.get(pk=help_id)
        help.status = new_status
        help.save()
        return JsonResponse({'success': True})
    except help.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'help not found'})
