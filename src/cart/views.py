from django.db.models import F
from django.views.generic import ListView
from django.core.exceptions import ValidationError

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

# from cart.services.cart_actions import (
#     add_product_to_cart,
#     get_cart_product_amt,
#     get_cart_product_list,
#     get_total_price,
#     remove_product_from_cart,
#     get_total_price,
#     change_cart_product_amt,
# )

from cart.serializer import CartSerializer, ProductSellerSerializer, CartPostSerializer

from products.models import SellerProduct
from cart.models import Cart


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

            context['total_price'] = 0
            for product in context['cart']:
                context['total_price'] += product['price'] * product['count']
            return context

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

        context['total_price'] = 0
        for product in context['cart']:
            context['total_price'] += product['price'] * product['count']
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
            for iter, item in enumerate(serializer.data):
                item['cart_count'] = cart_list[iter]['count']
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
                cart_list = [request.data]
                request.session['cart'] = cart_list
                return Response(200)
            for product in cart_list:
                if request.data['product_seller'] == product['product_seller']:
                    product['count'] += 1
                    print(cart_list)
                    request.session['cart'] = cart_list
                    return Response(200)
            cart_list.append(request.data)
            print(cart_list)
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
            except ValidationError as e:
                print(e)
            return Response(request.data)
        request.data['profile'] = request.user.pk
        return super().create(request)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            cart_list = request.session.get('cart')
            for product in cart_list:
                if int(kwargs['pk']) == product['product_seller']:
                    product['count'] = request.data['count']
                    request.session['cart'] = cart_list
                    return Response({'price': self.get_object().price, 'count': product['count']})

        try:
            self.get_object().clean(request.data['count'])
            return super().partial_update(request)
        except ValidationError as e:
            print(e)
            return Response(request.data)


class SellerApiViewSet(ModelViewSet):
    queryset = SellerProduct.objects.all().order_by('price')
    serializer_class = ProductSellerSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['product', 'seller']
