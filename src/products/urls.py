from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    ProductDetailsView,
    ProductsListView,
    ProductCreateView,
    ProductUpdateView,
)

app_name = "products"

urlpatterns = [
    path("products/", ProductsListView, name="products_list"),
    path("products/create/", ProductCreateView, name="product_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView, name="product_update"),
]
