import random

from django.core.cache import cache
from django.db.models import Min

from .models import Category, Product


FIXED_KEY = 'banners_fixed'
SLIDER_KEY = 'banners_slider'


class Banner:
    def __init__(self, fixed_amount=3, slider_amount=3):
        self.fixed = cache.get(FIXED_KEY)
        if not self.fixed:
            self.fixed = random.choices(
                Category.objects.all(),
                k=fixed_amount,
            )
            for category in self.fixed:
                category.sample = category.products.annotate(
                    min=Min('sellerproduct__price'),
                ).order_by('min').prefetch_related('images').all()[0]
            cache.set(FIXED_KEY, self.fixed)

        self.slider = cache.get(SLIDER_KEY)
        if not self.slider:
            self.slider = random.choices(
                Product.objects.all(),
                k=slider_amount,
            )
            cache.set(SLIDER_KEY, self.slider)
