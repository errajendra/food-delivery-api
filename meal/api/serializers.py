from rest_framework import serializers
from rest_framework.fields import empty
from ..models import (
    Category, SubCategory, Meal, Plan, PlanPurchase
)
from user.models import Address



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
    category = CategorySerilizer()
    sub_category = SubCategorySerilizer()
    class Meta:
        model = Meal
        fields = (
            'id', 'name', 'description', 'price', 'eating_type', 'category',
            'sub_category', 'image'
        )



""" Plan Listing Serializer."""
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = (
            'id', 'name', 'price', 'duration', 'saving_per_day', 'tag', 'eating_type'
        )



""" Plan Purchese Serilizer. """
class PlanPurcheseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanPurchase
        fields = ('plan', 'address')
