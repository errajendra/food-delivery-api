from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.shortcuts import get_object_or_404
from cc_avenue.utils import *
from pay_ccavenue import CCAvenue
from ..models import (
    Category, SubCategory, Meal, Plan, PlanPurchase, Transaction
)
from .serializers import (
    CategorySerilizer, SubCategorySerilizer, MealSerializer,
    PlanSerializer, PlanPurcheseSerializer, PlanPurcheseListSerializer,
)


""" Category Listing View."""
class CategoryView(viewsets.ModelViewSet):
    http_method_names = ('get',)
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerilizer



""" Sub Category Listing View."""
class SubCategoryView(viewsets.ModelViewSet):
    http_method_names = ('get',)
    serializer_class = CategorySerilizer
    
    def get_queryset(self):
        data = self.request.data
        categoryId = data['category'] if 'category' in data else None
        if categoryId:
            return SubCategory.objects.filter(category__id=categoryId).order_by('name')
        return SubCategory.objects.all()



""" Meal Listing and Detail View. """
class MealView(viewsets.ModelViewSet):
    http_method_names = ('get',)
    serializer_class = MealSerializer
    
    def get_queryset(self):
        data = self.request.GET
        eating_type = data['eating_type'] if 'eating_type' in data else None
        cat = data['category'] if 'category' in data else None
        subcat = data['sub_category'] if 'sub_category' in data else None
        search = data['search'] if 'search' in data else None
        qs = Meal.objects.select_related().all()
        if eating_type:
            qs = qs.filter(eating_type=eating_type)
        if cat:
            qs = qs.filter(category__id=cat)
        if subcat:
            qs = qs.filter(sub_category__id=subcat)
        if search:
            qs = qs.filter(Q(name__icontains=search)| Q(description__icontains=search))
        return qs



""" Plan View """
class PlanListingView(viewsets.ModelViewSet):
    http_method_names = ('get',)
    queryset = Plan.objects.all().order_by('-created_at')
    serializer_class = PlanSerializer



""" Plan Puchage View """
class PlanPurcheseView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ('post', 'get')
    
    def create(self, request, *args, **kwargs):
        serializer = PlanPurcheseSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            plan = serializer.validated_data['plan']
            address = serializer.validated_data['address']
            
            tnx = Transaction.objects.create(
                user = request.user,
                amount = plan.price
            )
            plan_purchage = PlanPurchase.objects.create(
                plan = plan,
                user = request.user,
                transaction = tnx,
                remaining_meals = plan.duration,
                address = address.full_address
            )
            # Create payment urls here
            ccavenue = CCAvenue(WORKING_KEY, ACCESS_CODE, MERCHANT_CODE, REDIRECT_URL, CANCEL_URL)
            p_currency = CURRENCY
            p_amount = str(tnx.amount)
            redirect_url = f"{request.scheme}://{request.META['HTTP_HOST']}{REDIRECT_URL}"
            cancel_url = f"{request.scheme}://{request.META['HTTP_HOST']}{CANCEL_URL}"
            p_customer_identifier = str(tnx.user.mobile_number)

            merchant_data={
                "currency" : p_currency ,
                'amount': p_amount,
                'redirect_url':redirect_url,
                'cancel_url': cancel_url,
                'order_id': str(tnx.id),
                'billing_name': tnx.user.name,
                'billing_tel': str(tnx.user.mobile_number),
                'billing_email': tnx.user.email,
                'billing_address': str(address.address1) + " " + str(address.address2),
                'billing_city': address.city,
                'billing_state': address.state,
                'billing_zip': address.zip,
                'billing_country': "India",
                'customer_identifier': p_customer_identifier,
                'merchant_param1': "PlanPurchase"
            }
            encryption = ccavenue.encrypt(merchant_data)
            cc_pay_url = f'https://{CC_PAY_MODE}.ccavenue.com/transaction/transaction.do?command=initiateTransaction&merchant_id={MERCHANT_CODE}&encRequest={encryption}&access_code={ACCESS_CODE}'
            # cc pay end
            
            return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "message": "Complete your payment.",
                    "data": {
                        "pay_url": cc_pay_url
                    }
                }
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "BAD REQUEST",
                "errors": serializer.errors
            }
        )       

    def list(self, request, *args, **kwargs):
        self.serializer_class = PlanPurcheseListSerializer
        self.queryset = PlanPurchase.objects.filter(
            user = request.user,
            status = True
        ).order_by('-remaining_meals')
        return super().list(request, *args, **kwargs)



""" 
    Plan Menu List 
    Meal list acording to user plan puchese
    Return Perticular meal list of plan
"""
class MenuListOfPlan(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ("get",)
    serializer_class = MealSerializer
        
    def list(self, request, *args, **kwargs):
        plan_id = self.request.GET.get('plan', None)
        if not plan_id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Give 'plan' Purchese plan id in parms"
                }
            )
        plan = get_object_or_404(PlanPurchase, id=plan_id)
        meals = Meal.objects.filter(
            eating_type = plan.plan.eating_type,
        )
        self.queryset = meals
        return super().list(request, *args, **kwargs)
