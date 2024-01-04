from django.urls import path

from .views import CreateOrderView

app_name = "cart"

urlpatterns = [
    path('create_order/', CreateOrderView.as_view(), name='create_order'),
]
