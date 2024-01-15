from cart.models import Cart


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
