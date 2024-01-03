from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from products.models import Product, SellerProduct

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


class Order(models.Model):
    """
    Модель для описания заказа покупателя.

    profile - связь с пользователем;
    fio - фамилия, имя и отчество покупателя;
    phone - телефон покупателя;
    email - адрес электронной почты покупателя;
    cart - связь с товарами в корзине;
    delivery_address - адрес доставки;
    delivery_type - способ доставки;
    payment_type - способ оплаты;
    comment - коментарий к заказу;
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False, blank=False, related_name='order')
    fio = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=14, unique=True, blank=True, null=True)
    email = models.EmailField(null=False, blank=False)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING, related_name='order')
    delivery_address = models.CharField(max_length=255, null=False, blank=False)
    delivery_type = models.CharField(default='обычная доставка', max_length=20)
    payment_type = models.CharField(max_length=40)
    comment = models.TextField(null=False, blank=True)
    archived = models.BooleanField(default=False)
