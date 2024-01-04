from django.urls import path

from .views import DiscountsListView

app_name = "discounts"

urlpatterns = [
    path('', DiscountsListView.as_view(), name='discounts_list'),
]

