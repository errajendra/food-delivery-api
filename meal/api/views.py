from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404
import json
from datetime import datetime, timedelta
from pytz import timezone
from razor_pay.utils import (
    client as razorpay_client,
    RAZOR_PAY_API_KEY
)
from ..models import (
    MealType, Meal, Plan, PlanPurchase, Transaction, MealRequestDaily,
    DailyMealMenu, CustomerSupport, Banner,
    SalesConnect, Coupan,
)
from .serializers import (
    MealTypeSerilizer, MealSerializer,MealTypeMenuSerilizer,
    PlanSerializer, PlanPurcheseListSerializer,
    DailyMealRequestSerializer, BannerSerializer, MealRequestDailySerializer,
    DailyMealMenuSerializer, MealTypePurcheseSerilizer,
    CustomerSupportSerializer,
    SalesConnectSerializer,
)
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from .exceptions import *


""" MealType Listing View."""
class MealTypeView(viewsets.ModelViewSet):
    http_method_names = ('get',)
    queryset = MealType.objects.all().order_by('name')
    serializer_class = MealTypeSerilizer
    
    def list(self, request, *args, **kwargs):
        plan_purchese = PlanPurchase.objects.filter(
            user=request.user, remaining_meals__gte=1, status=True
        ).values_list('plan')
        plan_type_purchese = MealType.objects.filter(
            id__in = Plan.objects.filter(id__in=plan_purchese).values_list('name')
        )
        other_plan_types = MealType.objects.exclude(
            id__in = plan_type_purchese.values_list('id')
        )
        data = {
            "status": status.HTTP_200_OK,
            "message": "OK",
            "results": {
                "purchese_types": MealTypePurcheseSerilizer(
                    plan_type_purchese, many= True,
                    context={'user':request.user}).data,
                "other_meal_types": MealTypeSerilizer(
                    other_plan_types, many= True).data
            }
        }
        # data = super().list(request, *args, **kwargs)
        plan_purchesed = plan_type_purchese.exists()
        if plan_purchesed:
            data['have_any_purchese_plan'] = True
        else:
            data['have_any_purchese_plan'] = False
        return Response(data)



""" Meal Listing and Detail View. """
class MealView(viewsets.ModelViewSet):
    http_method_names = ('get',)
    serializer_class = MealSerializer
    
    def get_queryset(self):
        data = self.request.GET
        eating_type = data['eating_type'] if 'eating_type' in data else None
        search = data['search'] if 'search' in data else None
        qs = Meal.objects.select_related().all()
        if eating_type:
            qs = qs.filter(eating_type=eating_type)
        if search:
            qs = qs.filter(Q(name__icontains=search)| Q(description__icontains=search))
        return qs



""" Plan View """
class PlanListingView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get',)
    serializer_class = PlanSerializer
    
    def get_queryset(self):
        name = self.request.GET.get('name')
        queryset = Plan.objects.filter(name__id=name).order_by('-created_at')
        return queryset



""" Plan Puchage View """
class PlanPurcheseView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ('post', 'get')
    
    def create(self, request, *args, **kwargs):
        data = request.data
        ids = data['plans']
        coupan_code = data.get("coupan_code", None)
        coupan = None
        if coupan_code:
            try:
                coupan = Coupan.objects.get(code=coupan_code, expiration_date__gte=datetime.now().date())
            except Coupan.DoesNotExist:
                return  Response(
                    {
                        "status": 400,
                        "message": "Coupon code is invalid."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                ) 
        plans = Plan.objects.filter(id__in=ids)
        if plans:
            price = plans.aggregate(Sum('price'))['price__sum']
            
            # Applying Discount
            if coupan:
                discount_type = coupan.discount_type 
                if discount_type == 'percentage':
                    discount_price = price * float(coupan.value) / 100 
                else:
                    discount_price = float(coupan.value)
                price = price - discount_price
            if not price or price < 1:
                raise APIException({'error': ("No plans selected or zero price")})
            
            # Create Transaction
            tnx = Transaction(
                user = request.user,
                amount = price,
            )
            if coupan:
                tnx.discount_code = coupan_code
                tnx.discount_amount = discount_price
            tnx.save()
            
            plan_purchage = []
            for plan in plans:
                plan_purchage.append(PlanPurchase(
                    plan = plan,
                    user = request.user,
                    transaction = tnx,
                    total_meals = plan.number_of_meals,
                    remaining_meals = plan.number_of_meals,
                ))
            PlanPurchase.objects.bulk_create(plan_purchage, batch_size=3)
            # Create payment urls here
            merchant_data={
                "currency" : "INR" ,
                'amount': tnx.amount * 100,
                'receipt': str(data['plans']),
            }
            payment = razorpay_client.order.create(merchant_data)
            tnx.tracking_id = payment['id']
            tnx.save()
            return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "message": "Complete your payment.",
                    "data": {
                        "order_detail": payment,
                        "murchent_detail": {
                            "key_id": RAZOR_PAY_API_KEY
                        }
                    }
                }
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "BAD REQUEST",
                "errors": """Pass valid plans ids in "{'plans':[1,2]}" formate."""
            }
        )       

    def list(self, request, *args, **kwargs):
        self.serializer_class = PlanPurcheseListSerializer
        self.queryset = PlanPurchase.objects.filter(
            user = request.user,
            status = True,
            remaining_meals__gt = 0
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
        eating_type = self.request.GET.get('eating_type', None)
        if not plan_id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Give 'plan' Purchese plan id in parms"
                }
            )
        plan = get_object_or_404(PlanPurchase, id=plan_id)
        eating_types = plan.plan.eating_type.split(',')
        eating_type_list = [eating.strip() for eating in eating_types]
        meals = Meal.objects.filter(
            eating_type__in = eating_type_list,
        )
        if eating_type:
            meals = meals.filter(eating_type=eating_type)
        self.queryset = meals
        return super().list(request, *args, **kwargs)



"""
Sales Connect Views
"""
class SalesConnectViews(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]
    serializer_class = SalesConnectSerializer
    def get_queryset(self):
        qs = SalesConnect.objects.filter(user=self.request.user)
        return qs



""" 
Daily meal order or Plan  meal order ViewSets
Get  User Daily/Plan meal orders.
"""
class PlanMeal(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ('post', 'get')

    def create(self, request, *args, **kwargs):
        created_meal_requests = []
        
        # Deserialize the input data using the serializer
        serializer = DailyMealRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            requester = user
            
            plan_purchese_id = serializer.validated_data['plan_purchese_id']
            meal_plan_data = serializer.validated_data['meal_plan_data']
            address = serializer.validated_data['address']
            instruction = serializer.validated_data.get('instruction', None)

            # Fetch the PlanPurchase instance based on plan_purchese_id
            try:
                plan_purchase = PlanPurchase.objects.get(pk=plan_purchese_id)
            except PlanPurchase.DoesNotExist:
                raise PlanPurchaseDoesNotExist()
            if len(meal_plan_data) > plan_purchase.remaining_meals:
                raise NoRemainMealsAvlSubscription()
            total_meal_comsumed = 0
            for meal_data in meal_plan_data:
                datetime = meal_data['datetime']
                meal_id = meal_data['meal']

                # Fetch the Meal instance based on meal_id
                try:
                    meal = Meal.objects.get(pk=meal_id)
                except Meal.DoesNotExist:
                    raise MealDoesNotExist()
                try:
                    meal_request = MealRequestDaily(
                        requester=requester,
                        plan=plan_purchase,
                        meal=meal,
                        date=datetime,
                        mobile_number = address.mobileNo,
                        address = address.full_address,
                        latitude = address.latitude,
                        longitude = address.longitude,
                        instruction = instruction
                    )
                    meal_request.save()
                    plan_purchase.remaining_meals = plan_purchase.remaining_meals - 1
                    plan_purchase.save()
                    total_meal_comsumed += 1
                    created_meal_requests.append({
                        "requester": meal_request.requester.id,
                        "plan": meal_request.plan.id,
                        "meal": MealSerializer(Meal.objects.get(id=meal_request.meal.id)).data,
                        "date": meal_request.date,
                        "status": meal_request.status,
                        "instruction": instruction,
                    })
                except IntegrityError:
                    # Handle the integrity error and provide a custom message
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Meal request already exists for this date and requester.",
                            "errors": {"meal_request": ["Meal request already exists for this date and requester."]}
                        }
                    )    
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "BAD REQUEST",
                    "errors": serializer.errors
                }
            )
        
        return Response(
            data={
                "status": status.HTTP_200_OK,
                "message": "Meal Requests submitted successfully.",
                "data": {
                    "meal_requests": created_meal_requests,
                    "remaining_meals": plan_purchase.remaining_meals,
                    "total_meal_comsumed": total_meal_comsumed
                }
            },
            status=status.HTTP_200_OK
        )



""" Home Page View. """
class BannerView(APIView):
    def get(self, request, format=None):
        banners = Banner.objects.filter(status=True)
        serializer = BannerSerializer(banners, many=True, context={'request':request})
        return Response(
            data={
                "status": status.HTTP_200_OK,
                "message": "Success.",
                "data": {
                    "banner": serializer.data,
                }
            },
            status=status.HTTP_200_OK
        )



""" Requested Plan Meal History. """
class RequestedPlanMealHistory(viewsets.ModelViewSet):
    http_method_names = ('get',)
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        user = self.request.user
        return MealRequestDaily.objects.filter(requester=user)
    
    
    def list(self, request, *args, **kwargs):
        now = datetime.now(timezone("Asia/Kolkata"))
        queryset = self.get_queryset()
        requested = queryset.filter(
            status="Requested",
            date__gte = now.date()
        )
        completed = queryset.filter(status="Success")
        canceled = queryset.filter(status="Cancelled")
        data = {
            "requested": MealRequestDailySerializer(requested, many=True).data,
            "completed": MealRequestDailySerializer(completed, many=True).data,
            "canceled": MealRequestDailySerializer(canceled, many=True).data
        }
        return Response(data)



""" Cancel Meal Request. """
class CancelMealRequest(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ("put",)
    serializer_class = MealRequestDailySerializer
    
    def get_queryset(self):
        return MealRequestDaily.objects.filter(requester=self.request.user)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        now = datetime.now(timezone("Asia/Kolkata"))
        ipd = instance.date - timedelta(days=1)
        c_time = datetime(
            year=now.year, month=now.month, day=now.day,
            hour=now.hour, minute=now.minute, second=now.second
        )
        ins_pre_date = datetime(
            year=ipd.year, month=ipd.month, day=ipd.day,
            hour=20, minute=0
        )
        if c_time < ins_pre_date:
            instance.status = "Cancelled"
            instance.save()
            plan = instance.plan
            plan.remaining_meals = plan.remaining_meals + 1
            plan.save()
        else:
            return Response(
                status=401,
                data={
                    "status":401,
                    "message": "You can cancel before 8 PM",})
        serializer = MealRequestDailySerializer(instance)
        return Response({"status":200, "message": "OK", "data": serializer.data})



""" 
Daily Meal Menu View
"""
class DailyMealMenuView(viewsets.ModelViewSet):
    http_method_names = ('get',)
    
    def get_queryset(self):
        start_date = datetime.strptime(
            self.request.GET.get('start_date') or datetime.now().date().strftime(
                "%Y-%m-%d"), "%Y-%m-%d")
        end_date = datetime.strptime(
            self.request.GET.get('end_date') or (
                datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"), "%Y-%m-%d"
            )
        qs = DailyMealMenu.objects.select_related().filter(
            date__gte = start_date, 
            date__lte = end_date
        ).order_by('date')
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        dates = qs.values_list('date', flat=True)
        data = {}
        for d in dates:
            date_qs = qs.filter(date=d)
            # date_meal_type = MealType.objects.filter(
            #     id__in = date_qs.values_list('meal_type', flat=True)
            #     ).values_list('name', flat=True)
            
            # data[f"{d}"] = {
            #     "meal_types": date_meal_type,
            #     "list": DailyMealMenuSerializer(date_qs, many=True).data
            # }
            
            data[f"{d}"] = DailyMealMenuSerializer(date_qs, many=True).data
        context = {
            "status": status.HTTP_200_OK,
            "message":"Successfully fetched daily meal menu.",
            "data": data
        }
        return Response(context)




""" Customer Support View. """
class CustomerSupportView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSupportSerializer
    
    def get_queryset(self):
        return CustomerSupport.objects.filter(user=self.request.user)
    
    
    def create(self, request, *args, **kwargs):
        user = request.user
        try:
            request.data['user'] = user.id
        except:
            request.data._mutable = True
            request.data['user'] = user.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": 200,
                    "message": "OK",
                    "data": serializer.data
                }
            )
        return Response(
            {
                "status": 400,
                "message": "BAD REQUEST",
                "errors": serializer.errors
            }
        )
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CustomerSupportSerializer(
            instance=instance, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": 200,
                    "message": "OK",
                    "data": serializer.data
                }
            )
        return Response(
            {
                "status": 400,
                "message": "BAD REQUEST",
                "errors": serializer.errors
            }
        )

