from django.db import models

from products.models import Product


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
    products = models.ManyToManyField(Product, through='CountProduct')
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.profile.name}"

class Profile(models.Model):
    name = models.CharField(max_length=20)
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/')


class CountProduct(models.Model):
    """
    Модель для описпания связи между товарами и продавцами,
    а также количества товаров у каждого продавца в наличии.

    product - связь с продуктами;
    seller - связь с продавцами;
    count - количество товаров в наличии.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    class Meta:
        ordering = ['seller', 'product']
