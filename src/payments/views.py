from django.http import HttpResponse
from django.shortcuts import render

from payments.services.payment_service import get_payment_status

from cart.models import Order


def payment_webhook_view(request):
    if request.method == 'GET':
        return HttpResponse(404)
    if request.method == 'POST':
        order = Order.object.get(payment_id=request.data[''])
        get_payment_status(order)
        return HttpResponse(200)
