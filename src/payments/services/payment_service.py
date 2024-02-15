from django.urls import reverse

from yookassa import Configuration, Payment
import uuid

from cart.services.cart_actions import clear_cart

from products.models import SellerProduct

from cart.models import Order

Configuration.account_id = '306183'
Configuration.secret_key = 'test_6EQxV_1iuGm1G3oircj-EAeRk4PZSRW3t1yTT6QU2ko'


def get_paid(order):
    return_url = reverse('cart:order_detail', args=(order.pk,))
    payment = Payment.create({
        "amount": {
            "value": str(order.total_price),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f'https://45.153.69.124{return_url}'
        },
        "capture": True,
        "test": True,
    }, uuid.uuid4())
    order.payment_id = payment.id
    order.save()
    return payment.confirmation.confirmation_url


def change_seller_product_count(cart):
    for product_seller, count in map(lambda product: (product['seller'], product['count']),
                                     cart.values()):
        seller = SellerProduct.objects.get(pk=product_seller)
        seller.count -= count
        seller.save()


def get_payment_status(order):
    change_seller_product_count(order.cart)
    if order == Order.objects.filter(profile=order.profile, archived=False).last():
        clear_cart(order.profile)
    order.status = True
    order.save()
