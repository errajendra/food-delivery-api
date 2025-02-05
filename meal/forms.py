from django import forms
from .models import (
    MealType, Meal, PlanPurchase,
    Plan, MealRequestDaily, DailyMealMenu,
    Banner, SalesConnect,
    Coupan, KitchenOffModel,
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
        exclude = ("status",)
        
        widgets = {
            'name': forms.Select(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_of_meals': forms.NumberInput(attrs={'class':'form-control'}),
            'tag': forms.Select(attrs={'class':'form-control'}),
            'validity': forms.NumberInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:  # Editing an existing instance
            self.fields['number_of_meals'].widget.attrs['readonly'] = True
            self.fields['number_of_meals'].widget.attrs['disabled'] = True
            # Optional: Add a class for styling
            self.fields['number_of_meals'].widget.attrs['class'] += ' readonly'



""" Plan Purchese Form. """
class PlanPurchaseForm(forms.ModelForm):
    
    class Meta:
        model = PlanPurchase
        fields = ('plan', 'user')
        
        widgets = {
            'plan': forms.Select(attrs={'class':'form-control'}),
            'user': forms.Select(attrs={'class':'form-control'}),
        }



""" Meal Request Form. """
class MealRequestForm(forms.ModelForm):
    class Meta:
        model = MealRequestDaily
        fields = ["plan", "meal", "date", "status", "mobile_number", "address",  "latitude", "longitude", "instruction"]
        
        widgets = {
            'plan': forms.Select(attrs={'class':'form-control'}),
            'meal': forms.Select(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'class':'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'instruction': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),

        }
        


""" Meal Request Update Form. """
class MealRequestUpdateForm(forms.ModelForm):
    class Meta:
        model = MealRequestDaily
        fields = ["meal", "status", "date", "mobile_number", "address", "latitude", "longitude"]
        
        widgets = {
            'meal': forms.Select(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
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



"""
    Sales Connect form
"""
class SalesConnectForm(forms.ModelForm):
    class Meta:
        model = SalesConnect
        fields = "__all__"
        
        widgets = {
            'user': forms.Select(attrs={'class':'form-control'}),
            'employee_id': forms.TextInput(attrs={'class':'form-control'}),
        }



"""
Coupon Form
"""
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupan
        fields = "__all__"
        
        widgets = {
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "discount_type": forms.Select(attrs={"class": "form-control"}),
            "value": forms.TextInput(attrs={"class": "form-control"}),
            "expiration_date": forms.DateInput(attrs={"class": "form-control", "type": "date"})
        }



""" Kitchen Off Form. """
class KitchenOffForm(forms.ModelForm):
    EATING_TYPE_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner')
    ]
    eating_types = forms.MultipleChoiceField(
        choices=EATING_TYPE_CHOICES,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )
    class Meta:
        model = KitchenOffModel
        fields = "__all__"
        
        widgets = {
            'date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }
