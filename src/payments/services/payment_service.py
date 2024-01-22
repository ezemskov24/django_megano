from django.shortcuts import redirect

from yookassa import Configuration, Payment
import uuid

from cart.services.cart_actions import clear_cart

Configuration.account_id = '306183'
Configuration.secret_key = 'test_6EQxV_1iuGm1G3oircj-EAeRk4PZSRW3t1yTT6QU2ko'


def get_paid(order):
    return_url = redirect('cart:order_detail', pk=order.pk)
    payment = Payment.create({
        "amount": {
            "value": str(order.total_price),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://127.0.0.1:8000{}".format(return_url.url)
        },
        "capture": True,
        "test": True,
    }, uuid.uuid4())
    order.payment_id = payment.id
    order.save()
    return payment.confirmation.confirmation_url


def change_seller_product_count(order):
    order_products = order.cart.select_related('product_seller')
    for order_product in order_products:
        order_product.product_seller.count -= order_product.count
        order_product.product_seller.save()


def get_payment_status(order):
    if order.status:
        return
    payment = Payment.find_one(order.payment_id)
    if payment.status == 'succeeded':
        change_seller_product_count(order)
        clear_cart(order.profile)
        order.status = True
        order.save()
