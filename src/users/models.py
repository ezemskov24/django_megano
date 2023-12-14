from django.db import models

from account.models import Profile
from products.models import Product, SellerProduct


class Seller(models.Model):
    """
    Модель для описания продавцов.

    name - название продавца;
    description - описание продавца;
    products - список продавакмых товаров;
    profile - связь с моделью профиля пользователя;
    archived - архивирование страницы продавца для мягкого удаления.
    """
    name = models.CharField(max_length=30)
    description = models.TextField()
    products = models.ManyToManyField(
        Product,
        through=SellerProduct,
        through_fields=('seller', 'product'),
        related_name='sellers',
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}"
