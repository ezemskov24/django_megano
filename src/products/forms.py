from django import forms


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
