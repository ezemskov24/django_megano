from django.core.exceptions import ValidationError
from django.db import models

from products.models import SellerProduct
from account.models import Profile


class Cart(models.Model):
    product_seller = models.ForeignKey(SellerProduct, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cart_profile')
    count = models.PositiveIntegerField(default=1)

    def clean(self, product_amt=0):
        if (product_amt > self.product_seller.count) \
                or ((self.count + 1 > self.product_seller.count) and (product_amt == 0)):
            raise ValidationError(
                    "Can't be more than total",
                )
