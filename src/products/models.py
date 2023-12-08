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


def category_images_directory_path(
        instance: "Category",
        filename: str
) -> str:
    'Сгенерировать путь для сохранения изображения'
    return "categories/images/category_{pk}/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


def category_icons_directory_path(
        instance: "Category",
        filename: str
) -> str:
    'Сгенерировать путь для сохранения иконки'
    return "categories/icons/category_{pk}/{filename}".format(
        pk=instance.pk,
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
    """
    Модель для описпания связи между товарами и продавцами,
    а также количества товаров и цены у каждого продавца в наличии.

    product - связь с продуктами;
    seller - связь с продавцами;
    count - количество товаров в наличии;
    price - цена товара у данного продавца.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    seller = models.ForeignKey(
        'users.Seller',
        on_delete=models.CASCADE,
    )
    count = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['seller', 'product']

    def __str__(self):
        return f'{self.product} by {self.seller}'


class Category(models.Model):
    """
    Класс категорий товаров
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True)
    is_active = models.BooleanField(default=True)
    parent_category = models.ForeignKey(
        'self',
        related_name='subcategories',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        validators=[validate_not_subcategory],
    )
    image = models.ImageField(
        upload_to=category_images_directory_path,
        null=True,
        blank=True,
    )
    icon = models.ImageField(
        upload_to=category_icons_directory_path,
        null=True,
        blank=True,
    )
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

    def get_absolute_url(self) -> str:
        'Получение абсолютной ссылки на категорию'
        return '#'

    def clean(self):
        if self.parent_category:
            if self.parent_category.pk == self.pk:
                raise ValidationError(
                    "Can't be a subcategory of itself",
                )
            if self.parent_category.parent_category:
                raise ValidationError(
                    "%(parent)s is a subcategory and can't be a parent",
                    params={'parent': self.parent_category},
                )
