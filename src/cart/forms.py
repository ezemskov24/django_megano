from django import forms

from .models import Order


class CreateOrderForm(forms.ModelForm):
    cart = forms.JSONField(widget=forms.Textarea(attrs={'hidden': True}))

    class Meta:
        model = Order
        fields = (
            'fio',
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
