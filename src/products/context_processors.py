from django.core.cache import cache

from . models import Category

from .services.compare_products import get_compare_list_amt


CATEGORIES_KEY = 'header_menu_categories'


def categories(request):
    active_categories = cache.get(CATEGORIES_KEY)
    if not active_categories:
        active_categories = Category.objects.filter(
            is_active=True).prefetch_related(
            'subcategories',
        ).all()
        cache.set(CATEGORIES_KEY, active_categories)
    return {
        'categories': active_categories,
    }


def product_compare_list_amt(request):
    compare_list_amt = get_compare_list_amt(request)
    return {
        'compare_amt': compare_list_amt,
    }
