from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .utils import client
from user.models import Transaction
from meal.models import PlanPurchase
from meal.api.serializers import PlanPurcheseListSerializer



""" Verify Payment signature """
@api_view(['POST'])
def verify_payment(request):
    razorpay_order_id = request.data['razorpay_order_id']
    razorpay_payment_id = request.data['razorpay_payment_id']
    razorpay_signature = request.data['razorpay_signature']
    try:
        result = client.utility.verify_payment_signature(
            {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
        )
    except Exception as ex:
        print(ex)
        return Response(
            data={
                'status': 400,
                'message': 'Invalid Payment.',
                'data': f"Signature not valid. - {ex}"
            },
            status=400
        )
    if result:
        tnx = get_object_or_404(Transaction, tracking_id=razorpay_order_id)
        tnx.status = "Success"
        tnx.razorpay_payment_id = razorpay_payment_id
        tnx.razorpay_signature = razorpay_signature
        tnx.save()
        plan = PlanPurchase.objects.filter(transaction=tnx)
        plan.update(status=True)
        plan_data = PlanPurcheseListSerializer(plan, many=True).data
        return Response(
            data={
                'status': 200,
                'message': 'Payment Success.',
                'payment_success': result,
                "data": plan_data
            },
            status=200
        )
    return Response(
        data={
            'status': 400,
            'message': 'Payment Not Captured.',
            'data': result
        },
        status=400
    )
