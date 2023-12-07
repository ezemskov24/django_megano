from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg, Min


from .validators import validate_not_subcategory


class Product(models.Model):
    """Модель продукта"""
    category = models.ForeignKey(
        "Category",
        related_name='products',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(max_length=200, unique=True, null=True)
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
        return '#'

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

    def description_short(self, length: int=100) -> str:
        if len(self.description) <= length:
            return self.description
        return self.description[:length] + '...'

    def name_short(self, length: int=50) -> str:
        if len(self.name) <= length:
            return self.name
        return self.name[:length] + '...'

    def __str__(self):
        return f'{self.name}'


def product_images_directory_path(
        instance: "ProductImage",
        filename: str
) -> str:
    'Сгенерировать путь для сохранения изображения продукта'
    return "products/images/product_{pk}/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


class Category(models.Model):
    """
    Класс категорий товаров
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    parent_category = models.ForeignKey('self', null=True, blank=True, related_name='children',
                                        on_delete=models.CASCADE)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    icon = models.ImageField(upload_to='category_icons/', null=True, blank=True)
    sort_index = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_index', 'name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

