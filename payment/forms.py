from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'shipping_full_name',
            'shipping_email',
            'shipping_phone',
            'shipping_addy',     # آدرس
            'shipping_state',
            'shipping_zipcode',
            'shipping_country',
        ]
        exclude = ['user']
        widgets = {
            'shipping_full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'shipping_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_addy': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_state': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_country': forms.TextInput(attrs={'class': 'form-control'}),
        }
