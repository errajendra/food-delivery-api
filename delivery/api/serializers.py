from rest_framework import serializers
from rest_framework.fields import empty
from meal.models import (
     MealRequestDaily
)

""" Daily Meal  Request Serializer. """
class MealRequestSerilizer(serializers.ModelSerializer):
    class Meta:
        model = MealRequestDaily
        fields = "__all__"