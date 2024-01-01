from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views.generic import ListView

from cart.services.cart_actions import (
    add_product_to_cart,
    get_cart_product_amt,
    get_cart_product_list,
    get_total_price,
    remove_product_from_cart,
    get_total_price,
    change_cart_product_amt,
)
from cart.models import Cart

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from cart.serializer import CartSerializer


class CartView(ListView):
    model = Cart
    template_name = 'cart/cart.jinja2'

    def get_queryset(self):
        return get_cart_product_list(self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        context['cart'] = [
            {
                'seller': cart_product.product_seller.pk,
                'slug': cart_product.product_name,
                'pict': cart_product.product_seller.product.images.first().image.url,
                'name': cart_product.product_seller.product.name,
                'price': cart_product.product_seller.price,
                'count': cart_product.count,
                'desc': cart_product.product_seller.product.description
            }
            for cart_product in context['object_list']
        ]

        context['total_price'] = get_total_price(self.request.user)
        return context


def add_product_to_cart_view(request, slug, pk):
    add_product_to_cart(request.user, slug, pk)
    return HttpResponse()


def cart_amt_view(request):
    return JsonResponse({'amt': get_cart_product_amt(request.user)})


def remove_product_from_cart_view(request, slug, pk):
    remove_product_from_cart(request.user, slug, pk)
    return HttpResponse(200)


def get_total_price_view(request):
    return JsonResponse({'price': get_total_price(request.user)})


def change_cart_product_amt_view(request, slug, change, pk):
    if change == 2:
        change = -1
    change_cart_product_amt(request.user, slug, change, pk)
    return HttpResponse()


class CartApiViewSet(ModelViewSet):
    serializer_class = CartSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['product_name', 'product_seller__seller']

    def get_queryset(self):
        return Cart.objects.filter(profile=self.request.user)

    def get_object(self):
        return Cart.objects.get(pk=self.kwargs['pk'])

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass


# class CartApiView(RetrieveUpdateDestroyAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_fields = ['product_name', 'product_seller']
