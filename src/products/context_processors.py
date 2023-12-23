from django.conf import settings
from django.core.cache import cache

from .forms import SearchForm
from .models import Category
from .utils import CacheableContextCategory

from .services.compare_products import get_compare_list_amt


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


def header_menu(request):
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

    return {
        'categories': menu_categories,
        'search_form': SearchForm()
    }


def product_compare_list_amt(request):
    compare_list_amt = get_compare_list_amt(request)
    return {
        'compare_amt': compare_list_amt,
    }
