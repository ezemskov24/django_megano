import random

from django.core.cache import cache
from django.db.models import Count, Min, Q

from .models import Category, Product


FIXED_KEY = 'banners_fixed'
SLIDER_KEY = 'banners_slider'


class Banner:
    def __init__(self, fixed_amount=3, slider_amount=3):
        self.fixed = cache.get(FIXED_KEY)
        if not self.fixed:
            self.fixed = random.choices(
                Category.objects.annotate(
                    num_products=Count('products', filter=Q(
                        products__archived=False))
                ).filter(is_active=True, num_products__gt=0).all(),
                k=fixed_amount,
            )
            for category in self.fixed:
                category.sample = category.products.filter(
                    archived=False,
                ).annotate(
                    min=Min('sellerproduct__price'),
                ).order_by('min').prefetch_related('images').all()[0]
            cache.set(FIXED_KEY, self.fixed)

        self.slider = cache.get(SLIDER_KEY)
        if not self.slider:
            self.slider = random.choices(
                Product.objects.filter(
                    archived=False,
                    category__is_active=True,
                ).all(),
                k=slider_amount,
            )
            cache.set(SLIDER_KEY, self.slider)
