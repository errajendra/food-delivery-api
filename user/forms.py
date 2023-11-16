from typing import Any
from django import forms
from .models import CustomUser as User




""" Profile Form. """
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "email","image", "mobile_number")
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
        }