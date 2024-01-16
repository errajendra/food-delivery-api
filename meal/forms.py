from django import forms
from .models import (
    Category, SubCategory, Meal, Meal,
    Plan, MealRequestDaily, DailyMealMenu
)


""" Category Form. """
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'})
        }



""" Sub Category Form. """
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = "__all__"
        
        widgets = {
            'category': forms.Select(attrs={'class':'form-control'}),
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'})
        }



""" Meal Form. """
class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = "__all__"
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'eating_type': forms.Select(attrs={'class':'form-control'}),
            # 'category': forms.Select(attrs={'class':'form-control'}),
            # 'sub_category': forms.Select(attrs={'class':'form-control'}),
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
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'duration': forms.NumberInput(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
           
            # 'saving_per_day': forms.NumberInput(attrs={'class':'form-control'}),
            'tag': forms.Select(attrs={'class':'form-control'}),
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
        fields = ['date', 'meals']
        
        widgets = {
            'date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'meals': forms.SelectMultiple(attrs={'class':'form-control'}),
        }
