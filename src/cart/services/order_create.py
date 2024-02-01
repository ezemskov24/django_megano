from cart.models import Cart
from discounts.services.discount_utils import calculate_discounted_prices

from adminsettings.models import SiteSettings


def get_total_price(carts) -> int:
    total_price = 0
    min_price = SiteSettings.objects.first().min_price_for_free_delivery
    delivery_price = SiteSettings.objects.first().delivery_cost
    for cart in carts.values():
        total_price += cart['price'] * cart['count']

    sellers = [cart['seller'] for cart in carts.values()]
    if not ((len(sellers) > 1 and (all(seller == sellers[0] for seller in sellers))) and total_price >= min_price):
        total_price += delivery_price
    return total_price


def get_fio(first_name: str, last_name: str, username: str) -> str:
    if last_name and first_name:
        fio = f"{last_name} {first_name}"
    elif last_name:
        fio = last_name
    elif first_name:
        fio = first_name
    else:
        fio = username

    return fio


def get_carts_JSON(carts):
    response = {}
    carts_list = [
        (cart.product_seller.product, cart.product_seller.price, cart.count)
        for cart in carts
    ]
    carts_list = calculate_discounted_prices(carts_list)
    for cart in carts_list:
        response[cart[0].id] = {
            'image': cart[0].images.first().image.url,
            'name': cart[0].name,
            'slug': cart[0].slug,
            'description': cart[0].description,
            'price': float(cart[2]),
            'count': cart[3],
            'seller': cart[0].sellerproduct_set.get(product=cart[0]).seller.name,
        }

    return response
