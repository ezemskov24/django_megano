from cart.models import Cart
from discounts.services.discount_utils import calculate_discounted_prices


def get_total_price(carts) -> int:
    total_price = 0
    for cart in carts.values():
        total_price += cart['price'] * cart['count']
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
    # carts_list = calculate_discounted_prices(carts_list)

    for cart in carts_list:
        response[cart[0].id] = {
            'image': cart[0].images.first().image.url,
            'name': cart[0].name,
            'slug': cart[0].slug,
            'description': cart[0].description,
            'price': cart[1],
            'count': cart[2],
        }

    return response
