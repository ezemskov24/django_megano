from django.urls import path

from payments.views import payment_webhook_view

app_name = "payments"

urlpatterns = [
    path('notification_url/', payment_webhook_view, name='payment_webhook')
]
