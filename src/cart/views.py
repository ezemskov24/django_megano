from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CreateOrderForm
from .models import Order, Cart


class CreateOrderView(LoginRequiredMixin, View):
    # login_url = reverse_lazy("account:login")
    # redirect_field_name = reverse_lazy("cart:create_order")

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
                'form': CreateOrderForm,
                'user_fio': fio,
                'user_phone': request.user.phone,
                'user_email': request.user.email,
                'carts': Cart.objects.all(),
            }
        else:
            content = {}

        print('============', content)
        return render(request, 'cart/create_order.jinja2', context=content)

    # def post(self, request, *args, **kwargs):
    #     print('============', request.POST)
