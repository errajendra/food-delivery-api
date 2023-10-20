from rest_framework import serializers
from ..models import (
    Category, SubCategory, Meal, Plan, PlanPurchase
)



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

