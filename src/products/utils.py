import random

from django.conf import settings
from django.core.cache import cache
from django.db.models import Count, Min, Q

from .models import Category, Product


FIXED_KEY = 'index_banners_fixed'
SLIDER_KEY = 'index_banners_slider'
TOP_SELLERS_KEY = 'index_top_sellers'


class CacheableContextProduct:
    def __init__(self, product: Product):
        self.name = product.name
        self.absolute_url = product.get_absolute_url()
        image = product.images.all()[0].image
        self.image_url = settings.MEDIA_URL + str(image) if image else ''


class CacheableContextCategory:
    def __init__(self, category: Category):
        self.name = category.name
        self.absolute_url = category.get_absolute_url()


class Banner:
    class SliderProduct(CacheableContextProduct):
        def __init__(self, product: Product):
            super().__init__(product)
            self.description = product.description

    class BannerCategory(CacheableContextCategory):
        def __init__(self, category: Category):
            super().__init__(category)
            sample = category.products.filter(
                archived=False,
            ).annotate(
                min=Min('sellerproduct__price'),
            ).order_by('min').prefetch_related('images').first()
            self.min_price = sample.min_price
            self.image_url = sample.images.first().image.url

    def __init__(self, fixed_amount=3, slider_amount=3):
        self.fixed = cache.get(FIXED_KEY)

        if not self.fixed:
            categories = Category.objects.annotate(
                    num_products=Count('products', filter=Q(
                        products__archived=False))
                ).filter(is_active=True, num_products__gt=0).all()

            if categories:
                random_categories = random.sample(
                    list(categories),
                    k=fixed_amount,
                )

                self.fixed = [self.BannerCategory(category)
                              for category in random_categories]

                cache.set(FIXED_KEY, self.fixed)

        self.slider = cache.get(SLIDER_KEY)

        if not self.slider:
            products = Product.objects.annotate(
                seller_count=Count('sellerproduct')
            ).filter(
                    archived=False,
                    category__is_active=True,
                    seller_count__gt=0,
                ).prefetch_related('images').all()
            if products:
                random_products = random.sample(
                    list(products),
                    k=slider_amount,
                )

                self.slider = [self.SliderProduct(product)
                               for product in random_products]
                cache.set(SLIDER_KEY, self.slider)


class TopSellerProduct(CacheableContextProduct):
    def __init__(self, product: Product):
        super().__init__(product)
        self.category = product.category.full_name
        self.price = product.min_price

    @staticmethod
    def get_top_sellers(amount=8):
        top_sellers = cache.get(TOP_SELLERS_KEY)
        if not top_sellers:
            products = Product.objects.annotate(
                seller_count=Count('sellerproduct')
            ).filter(
                archived=False,
                category__is_active=True,
                seller_count__gt=0,
            ).order_by(
                '-sort_index',
                '-count_sells',
            ).select_related(
                'category',
            ).prefetch_related('images').all()[:amount]
            top_sellers = [TopSellerProduct(product)
                           for product in products]
            cache.set(TOP_SELLERS_KEY, top_sellers)

        return top_sellers
