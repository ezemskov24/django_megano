from django.urls import path

from .views import (
    SellerDetailView,
)

app_name = "users"

urlpatterns = [
    # path("seller/create/", SellerCreateView.as_view(), name="seller_create"),
    path("seller/<int:pk>/", SellerDetailView.as_view(), name="seller_details"),
    # path("seller/", SellerDetailView.as_view(), name="seller_details"),
    # path("sellers/<int:pk>/update/", SellerUpdateView.as_view(), name="seller_update"),
]
