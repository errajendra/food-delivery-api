from rest_framework import serializers
from rest_framework.fields import empty
from ..models import (
    Category, SubCategory, Meal, Plan, PlanPurchase, MealRequestDaily
)
from user.models import Address
from user.api.serializers import TransactionSerializer



""" Category Listing Serializer. """
class CategorySerilizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')



""" Sub Category Listing Serializer. """
class SubCategorySerilizer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'category', 'name', 'description')



""" Meal Listing and Detail Serializer"""
class MealSerializer(serializers.ModelSerializer):
    # category = CategorySerilizer()
    # sub_category = SubCategorySerilizer()
    class Meta:
        model = Meal
        fields = (
            'id', 'name', 'description', 'price', 'eating_type', 'image'
        )



""" Plan Listing Serializer."""
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = (
            'id', 'name', 'price', 'duration', 'tag', 'eating_type'
        )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['price_per_meal'] = instance.price_per_meal
        return data



""" Plan Purchese Serilizer. """
class PlanPurcheseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanPurchase
        fields = ('plan', 'address')
    
    def validate_address(self, data):
        if not bool(data):
            raise serializers.ValidationError("Address is required.")
        elif Address.objects.filter(id=data).exists():
            return Address.objects.filter(id=int(data)).first()
        else:
            raise serializers.ValidationError('Invalid address id.')



""" User Plan Purchese List Serilizer. """
class PlanPurcheseListSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    transaction = TransactionSerializer()
    class Meta:
        model = PlanPurchase
        fields = "__all__"




class MealPlanDataSerializer(serializers.Serializer):
    datetime = serializers.DateTimeField()
    meal = serializers.IntegerField()

class DailyMealRequestSerializer(serializers.Serializer):
    plan_purchese_id = serializers.IntegerField()
    meal_plan_data = MealPlanDataSerializer(many=True)        
    


class BannerSerializer(serializers.Serializer):
    image_url = serializers.CharField()
    alt_text = serializers.CharField()    
    


class MealRequestDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = MealRequestDaily
        fields = "__all__"
