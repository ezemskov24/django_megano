from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Profile
import re


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ['email', 'password1', 'password2', 'username']


class ProfileForm(forms.ModelForm):
    phone = forms.CharField(max_length=17, required=False)

    def clean_phone(self):
        phone = self.cleaned_data['phone'][2:]
        cleaned_phone = re.sub(r'\D', '', phone[1:])
        return cleaned_phone

    class Meta:
        model = Profile
        fields = ['phone', 'avatar', 'username'] # , 'password'

