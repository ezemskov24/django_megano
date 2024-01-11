from django import forms

from .models import Order


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'fio', 'phone', 'email', 'city', 'delivery_address', 'delivery_type', 'payment_type', 'comment'
