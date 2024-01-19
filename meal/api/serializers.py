from rest_framework import serializers
from rest_framework.fields import empty
from ..models import (
    Category, SubCategory, Meal, Plan, PlanPurchase, MealRequestDaily,
    DailyMealMenu,
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
        try:
            user = self.context['request'].user
            plan_purchese = PlanPurchase.objects.filter(
                plan=instance, user=user, remaining_meals__gte=1, status=True
            ).exists()
            if plan_purchese:
                data['is_purchased'] = True
            else:
                data['is_purchased'] = False
        except:
            pass
        return data



""" Plan Purchese Serilizer. """
class PlanPurcheseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanPurchase
        fields = ('plan',)



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



#  the input data using the serializer
class DailyMealRequestSerializer(serializers.Serializer):
    plan_purchese_id = serializers.IntegerField()
    meal_plan_data = MealPlanDataSerializer(many=True)
    address = serializers.IntegerField()
    
    def validate_address(self, data):
        if not bool(data):
            raise serializers.ValidationError("Address is required.")
        elif Address.objects.filter(id=data).exists():
            return Address.objects.get(id=int(data))
        else:
            raise serializers.ValidationError('Invalid address id.')       
    


class BannerSerializer(serializers.Serializer):
    image_url = serializers.CharField()
    alt_text = serializers.CharField()    
    


class MealRequestDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = MealRequestDaily
        fields = "__all__"



class DailyMealMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyMealMenu
        fields = ["date", "meals"]
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['meals'] = MealSerializer(instance.meals.all(), many=True).data
        return data
