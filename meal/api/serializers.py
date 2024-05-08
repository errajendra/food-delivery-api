from rest_framework import serializers
from rest_framework.fields import empty
from ..models import (
    Meal, Plan, PlanPurchase, MealRequestDaily,
    DailyMealMenu, MealType,
    CustomerSupport,
    Banner,
    SalesConnect,
    Coupan as Coupon,
    KitchenOffModel,
)
from user.models import Address
from user.api.serializers import TransactionSerializer



""" Meal Listing and Detail Serializer"""
class MealTypeSerilizer(serializers.ModelSerializer):
    class Meta:
        model = MealType
        fields = (
            'id', 'name', 'description'
        )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        plans = Plan.objects.filter(name=instance).order_by('-number_of_meals')
        if plans:
            plan = plans[0]
            data['price_per_meal'] = plan.price_per_meal
            data['number_of_meals'] = plan.number_of_meals
            data['total_price'] = plan.number_of_meals * plan.price_per_meal
        else:
            data['price_per_meal'] = ""
            data['number_of_meals'] = ""
            data['total_price'] = " "
        return data



""" Meal Listing and Detail Serializer"""
class MealTypePurcheseSerilizer(MealTypeSerilizer):
    def to_representation(self, instance):
        customer = self.context.get('user')
        data = super().to_representation(instance)
        plans_purches = PlanPurchase.objects.filter(
            plan__name=instance, user=customer, status=True)
        data['plans_purches'] = PlanPurcheseListSerializer(plans_purches, many=True).data
        return data


""" Used on Meal Meanu Detail Serializer"""
class MealTypeMenuSerilizer(serializers.ModelSerializer):
    class Meta:
        model = MealType
        fields = (
            'id', 'name'
        )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        eating_types = instance.plans.all().values_list('eating_type', flat=True)
        eatings = []
        for et in eating_types:
            et = et.split(",")
            [eatings.append(i.strip()) for i in et]
        data['eating_types'] = set(eatings)
        return data
    
    

""" Meal Listing and Detail Serializer"""
class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = (
            'id', 'name', 'description', 'eating_type', 'image'
        )



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
    name = MealTypeSerilizer()
    class Meta:
        model = Plan
        fields = (
            'id', 'name', 'number_of_meals', 'price', 'tag', 'eating_type', 'validity'
        )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            data['price_per_meal'] = instance.price_per_meal
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
    instruction = serializers.CharField(required=False)
    
    def validate_address(self, data):
        if not bool(data):
            raise serializers.ValidationError("Address is required.")
        elif Address.objects.filter(id=data).exists():
            return Address.objects.get(id=int(data))
        else:
            raise serializers.ValidationError('Invalid address id.')       
    


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('image', 'alt')
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['image'] = self.context['request'].build_absolute_uri(instance.image.url)
        return data



class MealRequestDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = MealRequestDaily
        fields = "__all__"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['meal'] = MealSerializer(instance.meal).data
        try:
            data["meal_name"] = instance.plan.plan.name.name
            data["meal_description"] = instance.plan.plan.name.description
            data["eating_type"] = instance.plan.plan.eating_type
        except:
            pass
        return data



class DailyMealMenuSerializer(serializers.ModelSerializer):
    meal_type = MealTypeMenuSerilizer()
    class Meta:
        model = DailyMealMenu
        fields = ['date', 'meal_type', 'eating_type', 'items']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["eating_type"] = f"{data['meal_type']['name']} ({data['eating_type']})"
        return data



class CustomerSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSupport
        fields = ['user', 'attachment', 'message', 'created_at']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['status'] = instance.status
        return data



class SalesConnectSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = SalesConnect
        fields = "__all__"



class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ("code", "discount_type", "value", "expiration_date")



class KitchenOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenOffModel
        fields = ("date", "eating_types",)
