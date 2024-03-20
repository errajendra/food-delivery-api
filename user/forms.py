from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import CustomUser as User




""" Profile Form. """
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "email", "image", "mobile_number")
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly':''}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
        }



""" User by Admin Form. """
class UserAdminForm(forms.ModelForm):
        
    class Meta:
        model = User
        fields = (
            "email", "name", "image", "mobile_number",
            "is_active", "is_cook", "is_staff", "password",
        )
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly':''}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }



""" User by Admin Form. """
class AddCustummerForm(forms.ModelForm):
        
    class Meta:
        model = User
        fields = (
            "email", "mobile_number", "name", "image",
            "is_active",
        )
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
