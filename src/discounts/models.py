import decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count, Q
from django.utils.timezone import now

from products.models import Category, Product


class CurrentDiscountsManager(models.Manager):
    """ Менеджер актуальных скидок. """
    def get_queryset(self):
        return super().get_queryset().filter(active=True, end__gte=now())


def discount_images_directory_path(
        instance: "Category",
        filename: str
) -> str:
    """Сгенерировать путь для сохранения изображения."""
    return "discounts/images/category_{pk}/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Discount(models.Model):
    MIN_VALUE = 0.01

    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField()
    active = models.BooleanField(default=True)
    weight = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.CharField(max_length=100)

    discount_type = models.CharField(
        max_length=20,
        choices=[
            ('PRCNT', 'Percentage'),
            ('FXVAL', 'Fixed value'),
            ('PRC', 'Set price'),
        ],
    )
    value = models.DecimalField(max_digits=10, decimal_places=2)

    image = models.ImageField(
        upload_to=discount_images_directory_path,
        null=True,
        blank=True,
    )

    objects = models.Manager()
    current = CurrentDiscountsManager()

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['slug'])
        ]

    def clean(self, *args, **kwargs):
        super().clean()
        msg = None
        if not self.discount_type or not self.value:
            return

        if self.discount_type == 'PRCNT':
            if not 1 <= self.value <= 100:
                msg = 'Discount value must be from 1 to 100 %'
        elif self.value < 0.01:
            if self.discount_type == 'FXVAL':
                msg = f'Discount value can\'t be less than {self.MIN_VALUE}'
            else:
                msg = f'New price can\'t be less that {self.MIN_VALUE}'
        if msg:
            raise ValidationError({'value': msg})

    def get_discounted_price(self, price):
        if self.discount_type == 'PRCNT':
            return round(price * (100 - self.value) * decimal.Decimal(0.01), 2)
        elif self.discount_type == 'FXVAL':
            return max(price - self.value, self.MIN_VALUE)
        else:
            return self.value

    def __str__(self):
        return self.name

    @classmethod
    def get_active_count(cls):
        count = 0
        for subclass in cls.__subclasses__():
            query = subclass.objects.aggregate(
                active_count=Count(
                    'active',
                    filter=Q(active=True)
                )
            )
            count += query['active_count']
        return count


class ProductDiscount(Discount):
    products = models.ManyToManyField(
        Product,
        related_name='product_discounts',
    )


class CategoryDiscount(Discount):
    categories = models.ManyToManyField(
        Category,
        related_name='category_discounts',
    )


class BulkDiscount(Discount):
    product_amount = models.PositiveIntegerField()
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
