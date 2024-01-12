import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm

from .models import Profile


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ['email', 'password1', 'password2', 'username']


class ProfileForm(forms.ModelForm):
    phone = forms.CharField(max_length=17, required=False)
    new_password1 = forms.CharField(widget=forms.PasswordInput(), required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput(), required=False)

    def clean_phone(self):
        phone = self.cleaned_data['phone'][2:]
        cleaned_phone = re.sub(r'\D', '', phone[1:])
        if len(cleaned_phone) < 10:
            raise forms.ValidationError(f'Телефон должен содержать 10 символов, у вас - {len(cleaned_phone)}')
        return cleaned_phone

    class Meta:
        model = Profile
        fields = ['phone', 'avatar', 'username', 'new_password1', 'new_password2']    

