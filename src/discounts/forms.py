from django import forms


class DiscountForm(forms.Form):
    data = forms.JSONField()
