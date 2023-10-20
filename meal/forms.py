from django import forms
from .models import (
    Category, SubCategory, Meal, Meal,
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
            'category': forms.Select(attrs={'class':'form-control'}),
            'sub_category': forms.Select(attrs={'class':'form-control'}),
        }
