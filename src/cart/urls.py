from django.urls import path

from .views import (
    CartView,
    add_product_to_cart_view,
    cart_amt_view,
    remove_product_from_cart_view,
    get_total_price_view,
    change_cart_product_amt_view,
)


app_name = "cart"

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/<str:slug>/<int:pk>/', add_product_to_cart_view, name='add_to_cart'),
    path('amt/', cart_amt_view, name='cart_amt'),
    path('remove/<str:slug>/<int:pk>/', remove_product_from_cart_view, name='remove_from_cart'),
    path('total_price/', get_total_price_view, name='total_price'),
    path('change/<str:slug>/<int:change>/<int:pk>/', change_cart_product_amt_view, name='cart_product_change')
]
