from django.db import models


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
    # price = models.DecimalField(decimal_places=2, null=False)
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

    def average_discounted_price(self) -> int:
        'Получение средней цены со скидкой'

    def min_price(self) -> int:
        'Получение минимальной цены'

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
    )
