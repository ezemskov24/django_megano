from django.conf import settings
from django.core.cache import cache

from .models import Category
from .utils import CacheableContextCategory


CATEGORIES_KEY = 'header_menu_categories'


class MenuCategory(CacheableContextCategory):
    def __init__(self, category: Category):
        super().__init__(category)
        self.icon_url = settings.MEDIA_URL + str(
            category.icon,
        ) if category.icon else ''
        self.subcategories = [MenuCategory(subcategory)
                              for subcategory
                              in category.subcategories.filter(
                                  is_active=True
                              ).all()]


def categories(request):
    menu_categories = cache.get(CATEGORIES_KEY)

    if not menu_categories:
        active_categories = Category.objects.filter(
            is_active=True,
            parent_category=None,
        ).prefetch_related(
            'subcategories',
        ).all()
        menu_categories = [MenuCategory(category)
                           for category in active_categories]

        cache.set(CATEGORIES_KEY, menu_categories)

    for cat in menu_categories:
        print(cat.absolute_url)

    return {
        'categories': menu_categories,
    }
