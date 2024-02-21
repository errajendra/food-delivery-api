from django import forms
from .models import (
    MealType, Meal,
    Plan, MealRequestDaily, DailyMealMenu,
    Banner,
)


""" Meal Type Form. """
class MealTypeForm(forms.ModelForm):
    class Meta:
        model = MealType
        fields = "__all__"
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
        }



""" Meal Form. """
class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ("name", 'meal_type', 'eating_type', 'description', 'image')
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'eating_type': forms.Select(attrs={'class':'form-control'}),
            'meal_type': forms.Select(attrs={'class':'form-control'}),
        }



""" Plan Form. """
class PlanForm(forms.ModelForm):
    EATING_TYPE_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner')
    ]
    eating_type = forms.MultipleChoiceField(
        choices=EATING_TYPE_CHOICES,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )
    class Meta:
        model = Plan
        fields = "__all__"
        
        widgets = {
            'name': forms.Select(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_of_meals': forms.NumberInput(attrs={'class':'form-control'}),
            'tag': forms.Select(attrs={'class':'form-control'}),
            'validity': forms.NumberInput(attrs={'class':'form-control'}),
        }



""" Meal Request Form. """
class MealRequestForm(forms.ModelForm):
    class Meta:
        model = MealRequestDaily
        fields = ["requester", "plan", "meal", "status"]
        
        widgets = {
            
            'requester': forms.Select(attrs={'class':'form-control'}),
            'plan': forms.Select(attrs={'class':'form-control'}),
            'meal': forms.Select(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),

        }


class DailyMealMenuForm(forms.ModelForm):
    class Meta:
        model = DailyMealMenu
        fields = ['date', 'meal_type', 'eating_type', 'items']
        
        widgets = {
            'date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'meal_type': forms.Select(attrs={'class':'form-control'}),
            'eating_type': forms.Select(attrs={'class':'form-control'}),
        }


"""
Banner form used on Home Page of App
"""
class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = "__all__"
        
        widgets = {
            'alt': forms.TextInput(attrs={'class':'form-control'})
        }
