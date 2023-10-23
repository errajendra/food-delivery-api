from .utils import *
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from meal.models import (
    Transaction, PlanPurchase,
)

@api_view(['POST'])
def payment_verify(request):
    response = request.POST.get('encResp')
    response = decrypt(response, WORKING_KEY)
    dict_resp ={}
    for row in response.split('&'):
        key = row.split('=')[0]
        value = row.split('=')[1]
        dict_resp[key] = value

    order = Transaction.objects.get(id=int(dict_resp['order_id']))
    order.status_message = dict_resp['status_message']
    order.tracking_id = dict_resp['tracking_id']
    order.bank_id = dict_resp['bank_ref_no']
    order.card_name = dict_resp['card_name']
    order_status = dict_resp['order_status']
    
    if order_status == "Success":
        order.status="Success"
        order.save()
        plan = PlanPurchase.objects.get(transaction=order)
        plan.status = True
        plan.save()
        return redirect("keyparking://pay-success")
    elif order_status == "Aborted":
        order.status="Aborted"
        order.save()
        return redirect("keyparking://pay-failed")
    elif order_status == "Failure":
        order.status="Failed"
        order.save()
        return redirect("keyparking://pay-failed")
    
    return Response({
        'status': 200,
        'message':"""
            Payment recieved but order is not completed yet,
            please contact on helpline.
        """,
        'result': dict_resp
    })


@api_view(['POST'])
def payment_cancel(request): 
    response = request.POST.get('encResp')
    response = decrypt(response, WORKING_KEY)
    try:
        dict_resp ={}
        for row in response.split('&'):
            key = row.split('=')[0]
            value = row.split('=')[1]
            dict_resp[key] = value

        order = Transaction.objects.get(id=int(dict_resp['order_id']))
        order.status_message = dict_resp['status_message']
        order.tracking_id = dict_resp['tracking_id']
        order.bank_id = dict_resp['bank_ref_no']
        order.card_name = dict_resp['card_name']
        order.status="Aborted"
        order.save()
    except:
        pass
    return Response(response)
