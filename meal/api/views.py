from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ..models import (
    Category, SubCategory, Meal, Plan, PlanPurchase, Transaction
)
from .serializers import (
    CategorySerilizer, SubCategorySerilizer, MealSerializer,
    PlanSerializer, PlanPurcheseSerializer,
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
    http_method_names = ('post',)
    
    def create(self, request, *args, **kwargs):
        serializer = PlanPurcheseSerializer(data=request.data)
        if serializer.is_valid():
            plan = get_object_or_404(Plan, id=serializer.validated_data['plan'])
            return Response(serializer.data)
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Select Plan.",
                "errors": serializer.errors
            }
        )
        # tnx = Transaction.objects.create(
        #     user = request.user,
        #     amount = plan.price
        # )
        # plan_purchage = PlanPurchase(
        #     plan = plan,
        #     user = request.user,
        #     transaction = tnx,
        #     remaining_meals = plan.duration,
        #     address = ""
        # )
        
