from django import forms

from account.models import Seller
from products.models import SellerProduct


class FilterForm(forms.Form):
    price = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'range-line',
                'id': 'price',
                'type': 'text',
                'data-type': 'double',
                'data-min': '7',
                'data-max': '50',
                'data-from': '7',
                'data-to': '27',
            },
        ),
        required=False,
    )
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-input form-input_full',
                'id': 'title',
                'type': 'text',
                'placeholder': 'Название',
            },
        ),
        required=False,
    )
    in_stock = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'type': 'checkbox',
            },
        ),
        required=False,
    )


class SearchForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'search-input',
                'id': 'query',
                'name': 'query',
                'type': 'text',
                'placeholder': 'NVIDIA GeForce RTX 3060',
            },
        ),
    )


class SellerProductForm(forms.ModelForm):
    """
    Форма для создания SellerProduct через админ-панель.
    Если пользователь является superuser, то может видеть и менять любой товар.
    Продавец видит и меняет только свои.
    """
    class Meta:
        model = SellerProduct
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.request.user.is_superuser:
            self.fields['seller'].queryset = Seller.objects.filter(profile=self.request.user)
