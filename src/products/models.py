from django.db import models
from django.db.models import Avg, Min


class Product(models.Model):
    """Модель продукта"""
    category = models.ForeignKey(
        "Category",
        related_name='products',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(blank=True)
    manufacturer = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    count_sells = models.IntegerField(default=0)
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def get_absolute_url(self) -> str:
        'Получение абсолютной ссылки на продукт'

    def average_price(self) -> int:
        'Получение средней цены'
        avg_price = self.sellers.aggregate(
            avg=Avg('sellerproduct__price')
        ).get('avg')
        return round(avg_price, 2) if avg_price else 0.00

    def average_discounted_price(self) -> int:
        'Получение средней цены со скидкой'

    def min_price(self) -> int:
        'Получение минимальной цены'
        min_price = self.sellers.aggregate(
            min=Min('sellerproduct__price')
        ).get('min')
        return round(min_price, 2) if min_price else 0.00

    def __str__(self):
        return f'{self.name}'


def product_images_directory_path(
        instance: "ProductImage",
        filename: str
) -> str:
    'Сгенерировать путь для сохранения изображения'
    return "products/images/product_{pk}/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


class Picture(models.Model):
    """Модель изображения продукта"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(upload_to=product_images_directory_path)


class SellerProduct(models.Model):
    """Модель связи продавца и продукта"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    seller = models.ForeignKey(
        'Seller',
        on_delete=models.CASCADE,
    )
    count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product} by {self.seller}'


class Category(models.Model):
    """Category placeholder"""
    title = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f'{self.title}'


class Seller(models.Model):
    """Seller placeholder"""
    products = models.ManyToManyField(
        Product,
        through=SellerProduct,
        through_fields=('seller', 'product'),
        related_name='sellers',
    )

    def __str__(self):
        return f'Seller #{self.pk}'
