from decimal import Decimal

from django.db.models import Avg, Q, Min
from django.utils.timezone import now


def _get_discount(product: 'Product'):
    """ Получение действующей на продукт скидки. """
    product_disount = product.product_discounts.filter(
        Q(start=None) | Q(start__lte=now()),
        active=True,
        end__gte=now(),
    ).order_by('weight').first()

    category_discount = product.category.category_discounts.filter(
        Q(start=None) | Q(start__lte=now()),
        active=True,
        end__gte=now(),
    ).order_by('weight').first()

    if product_disount and category_discount:
        if category_discount.weight > product_disount.weight:
            return category_discount
        else:
            return product_disount
    else:
        return product_disount or category_discount


def get_average_price(product: 'Product') -> Decimal:
    """ Средняя цены продукта. """
    avg_price = product.sellers.aggregate(
        avg=Avg('sellerproduct__price')
    ).get('avg')
    return round(avg_price, 2) if avg_price else 0.00


def discounted_average_price(product: 'Product') -> Decimal:
    """ Средняя цены продукта со скидкой. """
    avg_price = get_average_price(product)

    discount = _get_discount(product)

    if discount:
        return round(discount.get_discounted_price(avg_price), 2)
    return avg_price


def get_min_price(product: 'Product') -> Decimal:
    """ Минимальная цена продукта. """
    min_price = product.sellers.aggregate(
        min=Min('sellerproduct__price')
    ).get('min')
    return round(min_price, 2) if min_price else 0.00


def get_discounted_min_price(product: 'Product') -> Decimal:
    """ Минимальная цены продукта со скидкой. """
    min_price = product.min_price

    discount = _get_discount(product)

    if discount:
        return round(discount.get_discounted_price(min_price), 2)
    return min_price
