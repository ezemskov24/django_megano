from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CartView,
    add_product_to_cart_view,
    cart_amt_view,
    remove_product_from_cart_view,
    get_total_price_view,
    change_cart_product_amt_view,
    CartApiViewSet,
    SellerApiViewSet,
)


app_name = "cart"

router = DefaultRouter()
router.register(r'cart', CartApiViewSet, basename='cart_api')
router.register(r'product-seller', SellerApiViewSet, basename='product_seller_api')
print(DefaultRouter.routes)

urlpatterns = [
    path('', CartView.as_view(), name='cart_view'),
    path('add/<str:slug>/<int:pk>/', add_product_to_cart_view, name='add_to_cart'),
    path('amt/', cart_amt_view, name='cart_amt'),
    path('remove/<str:slug>/<int:pk>/', remove_product_from_cart_view, name='remove_from_cart'),
    path('total_price/', get_total_price_view, name='total_price'),
    path('change/<str:slug>/<int:change>/<int:pk>/', change_cart_product_amt_view, name='cart_product_change'),
    path('api/', include(router.urls)),
]

