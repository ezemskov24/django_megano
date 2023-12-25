from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (
    UserLogoutView,
    UserLoginView,
    RegisterView,
    UserAccountView,
    ProfileUpdateView,
    UserEmailView,
    SellerDetailView
)

app_name = 'account'

urlpatterns = [
    path('login/', UserLoginView, name='login'),
    # path(
    #     'login/',
    #     LoginView.as_view(
    #         template_name="registration/login.jinja2",
    #         redirect_authenticated_user=True,
    #     ),
    #     name="login",
    # ),
    path('registr/', RegisterView.as_view(), name='registr'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('e-mail/', UserEmailView.as_view(), name='e-mail'),
    path("seller/<int:pk>/", SellerDetailView.as_view(), name="seller_details"),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('account/', UserAccountView.as_view(), name='account'),
]
