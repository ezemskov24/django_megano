from django.urls import path

from .views import (
    ProductDetailsView,
    ProductsListView,
    ProductCreateView,
    ProductUpdateView,
    ProductsCompareView,
    IndexView,
)

app_name = "products"

urlpatterns = [
    path("products/", ProductsListView, name="products_list"),
    path("products/create/", ProductCreateView, name="product_create"),
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView, name="product_update"),
    path('compare/', ProductsCompareView.as_view(), name='product_compare'),
    path("", IndexView.as_view(), name="index"),
]
