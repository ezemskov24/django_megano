from django.db import models

from products.models import Product, SellerProduct

from account.models import Profile


class Cart(models.Model):
    product_name = models.SlugField(max_length=200, null=True)
    product_seller = models.ForeignKey(SellerProduct, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cart_profile')
    count = models.IntegerField(
        default=1,
        validators=[

        ]
    )

    # def __str__(self):
    #     return self.product.name
