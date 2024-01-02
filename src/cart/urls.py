from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CartView,
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
    path('api/', include(router.urls)),
]

