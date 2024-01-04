from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from .forms import CreateOrderForm
from .models import Order


class CreateOrderView(View):
    # model = Order
    # template_name = 'cart/create_order.jinja2'
    # fields = 'fio', 'phone', 'email', 'cart', 'delivery_address', 'delivery_type', 'payment_type', 'comment'
    # success_url = reverse_lazy("account:account")

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            last_name = request.user.last_name
            first_name = request.user.first_name
            if last_name and first_name:
                fio = f"{last_name} {first_name}"
            elif last_name:
                fio = last_name
            elif first_name:
                fio = first_name
            else:
                fio = request.user.username

            content = {
                'form': CreateOrderForm(),
                'user_fio': fio,
                'user_phone': request.user.phone,
                'user_email': request.user.email,
            }
        else:
            content = {}

        return render(request, 'cart/create_order.jinja2', context=content)


