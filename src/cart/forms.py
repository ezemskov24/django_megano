import logging

import phonenumbers as phonenumbers
from django import forms

from .models import Order
import phonenumbers


class CreateOrderForm(forms.Form):
    fio = forms.CharField(max_length=255, required=True)
    cart = forms.JSONField(widget=forms.Textarea(attrs={'hidden': True}))
    phone = forms.CharField(required=True)

    class Meta:
        model = Order
        fields = (
            'phone',
            'email',
            'city',
            'cart',
            'delivery_address',
            'delivery_type',
            'payment_type',
            'comment',
            'total_price'
        )

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        z = phonenumbers.parse(phone, "SG")
        if not phonenumbers.is_valid_number(z):
            raise forms.ValidationError("Number not in successful format")
        return z.national_number
