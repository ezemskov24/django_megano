from cart.models import Cart
from discounts.services.discount_utils import calculate_discounted_prices


def get_total_price(carts: Cart) -> int:
    total_price = 0
    for cart in carts:
        total_price += cart.product_seller.price * cart.count

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


def get_cart_JSON(carts):
    response = []
    carts_list = [
        (cart.product_seller.product, cart.product_seller.price, cart.count)
        for cart in carts
    ]
    # carts_list = calculate_discounted_prices(carts_list)

    for cart in carts:
        response.append({
            'image': cart.product_seller.product.images.first().image,
            'name': cart.product_seller.product.name,
            'description': cart.product_seller.product.description,
            'price': cart.product_seller.price,
            'count': cart.count,
        })

    return response
