from django.core.cache import cache

from . models import Category


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
