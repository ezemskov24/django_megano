from django.core.exceptions import ValidationError

from cart.models import Cart
from products.models import SellerProduct
from rest_framework.response import Response


def merge_cart_products(user, cart_list_session):
    for product_session in cart_list_session:
        product, created = Cart.objects.get_or_create(
            profile=user,
            product_seller__pk=product_session['product_seller'],
            defaults={
                'product_seller': SellerProduct.objects.get(pk=product_session['product_seller']),
                'count': product_session['count'],
                'profile': user,
            }
        )
        if not created:
            try:
                product.clean(product.count + product_session['count'])
                product.count += product_session['count']
                product.save()
            except ValidationError:
                product.count = product.product_seller.count
                product.save()
