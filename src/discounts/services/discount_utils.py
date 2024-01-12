import decimal

from django.db import models


class DiscountTypeEnum(models.TextChoices):
    PERCENTAGE = 'PRCNT', 'Percentage'
    FIXED_VALUE = 'FXVAL', 'Fixed value'
    SET_PRICE = 'PRC', 'Set price'


def get_discounted_price(discount, price):
    if discount.discount_type == DiscountTypeEnum.PERCENTAGE:
        return round(price * (100 - discount.value) * decimal.Decimal(0.01), 2)
    elif discount.discount_type == DiscountTypeEnum.FIXED_VALUE:
        return max(price - discount.value, discount.MIN_VALUE)
    else:
        return discount.value
