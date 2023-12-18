from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Profile

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ['email', 'password1', 'password2', 'username']


# class ProfileUpdateForm(UserChangeForm):
#     class Meta:
#         model = Profile
#         fields = ['phone', 'avatar']


class ProfileForm(forms.ModelForm):


    class Meta:
        model = Profile
        fields = ['phone', 'avatar'] # 'username',, 'password'

