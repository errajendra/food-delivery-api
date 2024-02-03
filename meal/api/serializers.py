from rest_framework import serializers
from rest_framework.fields import empty
from ..models import (
    Meal, Plan, PlanPurchase, MealRequestDaily,
    DailyMealMenu,
)
from user.models import Address
from user.api.serializers import TransactionSerializer



""" Meal Listing and Detail Serializer"""
class MealSerializer(serializers.ModelSerializer):
    # category = CategorySerilizer()
    # sub_category = SubCategorySerilizer()
    class Meta:
        model = Meal
        fields = (
            'id', 'name', 'description', 'eating_type', 'image'
        )



""" Plan Listing Serializer."""
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = (
            'id', 'name', 'price', 'tag', 'eating_type', 'validity'
        )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            user = self.context['request'].user
            plan_purchese = PlanPurchase.objects.filter(
                plan=instance, user=user, remaining_meals__gte=1, status=True
            )
            if plan_purchese.exists():
                data['is_purchased'] = True
                data['remaining_meals'] = plan_purchese.first().remaining_meals
            else:
                data['is_purchased'] = False
        except:
            pass
        return data



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
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['meal'] = MealSerializer(instance.meal).data
        return data



class DailyMealMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyMealMenu
        fields = ["date", "meals"]
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['meals'] = MealSerializer(instance.meals.all(), many=True).data
        return data
