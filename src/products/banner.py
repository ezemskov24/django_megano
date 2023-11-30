import random

from django.db.models import Min
from django.db.models.functions import Round

from .models import Category, Product


class Banner:
    def __init__(self, fixed_amount=3, slider_amount=3):
        self.fixed = random.choices(Category.objects.all(), k=fixed_amount)
        for category in self.fixed:
            category.sample = category.products.annotate(
                min=Min('sellerproduct__price'),
            ).order_by('min').prefetch_related('images').get()

        self.slider = random.choices(Product.objects.all(), k=fixed_amount)
