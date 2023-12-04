from django.urls import path

from .views import (
    SellersListView,
    SellerDetailView,
)

app_name = "users"

urlpatterns = [
    path("sellers/", SellersListView.as_view(), name="sellers_list"),
    # path("seller/create/", SellerCreateView.as_view(), name="seller_create"),
    path("sellers/<int:pk>/", SellerDetailView.as_view(), name="seller_details"),
    # path("sellers/<int:pk>/update/", SellerUpdateView.as_view(), name="seller_update"),
]
