from django.urls import path
from .views import UserLogoutView, UserLoginView, RegisterView, UserAccountView, ProfileUpdateView

app_name = 'account'

urlpatterns = [
    path('login/', UserLoginView, name='login'),
    path('registr/', RegisterView.as_view(), name='registr'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('account/', UserAccountView.as_view(), name='account'),
]