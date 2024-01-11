import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm

from .models import Profile


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ['email', 'password1', 'password2', 'username']


class ProfileForm(forms.ModelForm): #, SetPasswordForm
    phone = forms.CharField(max_length=17, required=False)
    new_password1 = forms.CharField(widget=forms.PasswordInput(), required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput(), required=False)

    # def clean_password(self):
    #     print('password_form = ', self.cleaned_data['new_password1'], '!')
    #     new_password1 = self.cleaned_data['new_password1']
    #     new_password2 = self.cleaned_data['new_password1']
    #     if new_password1:
    #         if len(new_password1) < 6:
    #             raise forms.ValidationError('Пароль должен содержать не менее 6 символов.')
    #     return new_password1, new_password2

    # def clean_password(self):
    #     password = self.cleaned_data['new_password1']
    #     print('password_form = ', password, '!')
    #     if password:
    #         if len(password) < 6:
    #             raise forms.ValidationError('Пароль должен содержать не менее 6 символов.')
    #     else:
    #         raise forms.ValidationError('Пароль должен содержать не менее 6 символов.')
    #     return password

    def clean_phone(self):
        phone = self.cleaned_data['phone'][2:]
        cleaned_phone = re.sub(r'\D', '', phone[1:])
        if len(cleaned_phone) < 10:
            raise forms.ValidationError(f'Телефон должен содержать 10 символов, у вас - {len(cleaned_phone)}')
        return cleaned_phone

    class Meta:
        model = Profile
        fields = ['phone', 'avatar', 'username', 'new_password1', 'new_password2']    #, 'password1', 'new_password2']    # , 'password'



# class ChangePasswordForm(UserChangeForm):
#     new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['new_password'])
#         if commit:
#             user.save()
#         return user
