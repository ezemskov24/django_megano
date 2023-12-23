from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    ProductDetailsView,
    ProductsListView,
    ProductCreateView,
    ProductUpdateView,
    ProductsCompareView,
    # PropertyCreateView,
    index_view,
    ProductsCompareViewSet,
    delete_all_compare_products_view,
    delete_product_to_compare_list_view,
)

app_name = "products"

routers = DefaultRouter()
routers.register('compare_products', ProductsCompareViewSet, basename='ProductsCompare')

urlpatterns = [
    path("products/", ProductsListView, name="products_list"),
    path("products/create/", ProductCreateView, name="product_create"),
    path("<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update/", ProductUpdateView, name="product_update"),
    path('compare/', ProductsCompareView.as_view(), name='product_compare'),
    # path('create/', PropertyCreateView.as_view(), name='create'),
    path('compare/delete_all/', delete_all_compare_products_view, name='delete_all_compare_products'),
    path('compare/delete/<int:pk>/', delete_product_to_compare_list_view, name='delete_product_to_compare_list'),
    path("", index_view, name="index"),
    path('api/', include(routers.urls)),
]
