from django.contrib.auth.views import LoginView
from django.urls import path
from .views import UserLogoutView, UserProfileView, UserLoginView, SellerDetailView, UserBrowsingHistoryView

# from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'account'

urlpatterns = [
    path('login/', UserLoginView, name='login'),
    # path('login/', LoginView.as_view(template_name='registration/login.jinja2'), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/browsing-history', UserBrowsingHistoryView.as_view(), name='browsing_history'),
    path("seller/<int:pk>/", SellerDetailView.as_view(), name="seller_details"),
]
