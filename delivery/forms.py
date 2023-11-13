from django import forms
from user.models import CustomUser 

""" Delivery Person  Form. """
class DeliveryPersonForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("name", "email", "password", "mobile_number")
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }