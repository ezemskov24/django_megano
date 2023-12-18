from django.contrib.auth.views import LoginView
from django.urls import path
from .views import UserLogoutView, UserLoginView, RegisterView, UserAccountView, ProfileUpdateView #registr UserProfileView   profile
# from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'account'

urlpatterns = [
    path('login/', UserLoginView, name='login'),
    path('registr/', RegisterView.as_view(), name='registr'),
    # path('registr/', registr, name='registr'),
    # path('login/', LoginView.as_view(template_name='registration/login.jinja2'), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    # path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    # path('profile/', profile, name='profile'),
    path('account/', UserAccountView.as_view(), name='account'),
]