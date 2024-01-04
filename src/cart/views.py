from django.db.models import F
from django.views.generic import ListView
from django.core.exceptions import ValidationError

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from cart.serializer import CartSerializer, ProductSellerSerializer, CartPostSerializer

from products.models import SellerProduct
from cart.models import Cart
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


class CartView(ListView):
    model = Cart
    template_name = 'cart/cart.jinja2'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            cart_list = self.request.session.get('cart')
            if cart_list is None:
                return []
            return [[SellerProduct.objects.get(pk=obj['product_seller']), obj['count']] for obj in cart_list]

        return Cart.objects.filter(profile=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        if not self.request.user.is_authenticated:
            context['cart'] = [
                {
                    'product_obj': product_seller[0].product,
                    'pk': product_seller[0].pk,
                    'seller': product_seller[0].pk,
                    'pict': product_seller[0].product.images.first().image.url,
                    'name': product_seller[0].product.name,
                    'price': product_seller[0].price,
                    'count': product_seller[1],
                    'desc': product_seller[0].product.description
                }
                for product_seller in context['object_list']
            ]
        else:
            context['cart'] = [
                {
                    'product_obj': cart_product.product_seller.product,
                    'pk': cart_product.pk,
                    'seller': cart_product.product_seller.pk,
                    'pict': cart_product.product_seller.product.images.first().image.url,
                    'name': cart_product.product_seller.product.name,
                    'price': cart_product.product_seller.price,
                    'count': cart_product.count,
                    'desc': cart_product.product_seller.product.description
                }
                for cart_product in context['object_list']
            ]

        context['total_price'] = sum(map(lambda product: product['price'] * product['count'], context['cart']))
        return context


class CartApiViewSet(ModelViewSet):
    def get_serializer_class(self):
        if not self.request.user.is_authenticated:
            return ProductSellerSerializer

        if self.request.method == 'POST' or self.request.method == 'PUT':
            return CartPostSerializer
        return CartSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            cart_list = self.request.session.get('cart')
            if cart_list is None:
                return []
            return [SellerProduct.objects.get(pk=obj['product_seller']) for obj in cart_list]

        return Cart.objects.filter(profile=self.request.user)

    def get_object(self):
        if not self.request.user.is_authenticated:
            return SellerProduct.objects.get(pk=self.kwargs['pk'])

        return Cart.objects.filter(profile=self.request.user).get(pk=self.kwargs['pk'])

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            cart_list = request.session.get('cart')
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            for item, cart_product in zip(serializer.data, cart_list):
                item['cart_count'] = cart_product['count']
            return Response(serializer.data)

        return super().list(request)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            cart_list = request.session.get('cart')
            for product in cart_list:
                if int(kwargs['pk']) == product['product_seller']:
                    cart_list.remove(product)
                    request.session['cart'] = cart_list
                    return Response(200)
            return Response(400)

        return super().destroy(request)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            cart_list = request.session.get('cart')
            if cart_list is None:
                request.session['cart'] = [request.data]
                return Response(200)
            for product in cart_list:
                if request.data['product_seller'] == product['product_seller']:
                    try:
                        if product['count'] + 1 > SellerProduct.objects.get(pk=request.data['product_seller']).count:
                            raise ValidationError("Can't be more than total")
                        product['count'] += 1
                        request.session['cart'] = cart_list
                    except ValidationError:
                        return Response(400)
                    return Response(200)
            cart_list.append(request.data)
            request.session['cart'] = cart_list
            return Response(200)

        cart_product = Cart.objects.filter(
            profile=request.user,
            product_seller=request.data['product_seller']
        )
        if cart_product:
            try:
                cart_product[0].clean()
                cart_product.update(count=F('count') + 1)
            except ValidationError("Can't be more than total"):
                pass
            return Response(request.data)
        request.data['profile'] = request.user.pk
        return super().create(request)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            cart_list = request.session.get('cart')
            for product in cart_list:
                if int(kwargs['pk']) == product['product_seller']:
                    try:
                        if request.data['count'] > self.get_object().count:
                            raise ValidationError("Can't be more than total")
                        product['count'] = request.data['count']
                        request.session['cart'] = cart_list
                    except ValidationError:
                        pass
                    return Response({'price': self.get_object().price, 'count': product['count']})

        try:
            self.get_object().clean(request.data['count'])
            return super().partial_update(request)
        except ValidationError:
            return Response(request.data)


class SellerApiViewSet(ModelViewSet):
    queryset = SellerProduct.objects.all().order_by('price')
    serializer_class = ProductSellerSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['product', 'seller']

