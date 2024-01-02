from django.db.models import F
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
from rest_framework import status

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from cart.serializer import CartSerializer

from cart.serializer import ProductSellerSerializer, CartPostSerializer

from products.models import SellerProduct


class CartView(ListView):
    model = Cart
    template_name = 'cart/cart.jinja2'

    def get_queryset(self):
        return get_cart_product_list(self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        context['cart'] = [
            {
                'product_obj': cart_product.product_seller.product,
                'pk': cart_product.pk,
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


class CartApiViewSet(ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['product_name', 'product_seller__seller']

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return CartPostSerializer
        return CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(profile=self.request.user)

    def get_object(self):
        return Cart.objects.filter(profile=self.request.user).get(pk=self.kwargs['pk'])

    def create(self, request, *args, **kwargs):
        cart_product = Cart.objects.filter(
            profile=request.user,
            product_seller=request.data['product_seller']
        )
        if cart_product:
            cart_product.update(count=F('count') + 1)
            return Response(request.data)
        request.data['profile'] = request.user.pk
        return super().create(request)


class SellerApiViewSet(ModelViewSet):
    queryset = SellerProduct.objects.all().order_by('price')
    serializer_class = ProductSellerSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['product', 'seller']
