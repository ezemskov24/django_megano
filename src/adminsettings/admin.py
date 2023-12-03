from django.contrib import admin, messages
from django.core.cache import cache

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'reviews_count',
        'products_per_page',
        'delivery_cost',
        'express_delivery_cost',
        'discount_percentage',
        'products_images',
        'amount_products_from_the_seller'
    ]

    actions = ['reset_cache_action']

    def reset_cache_action(self, request, queryset):
        cache.clear()
        self.message_user(request, ("Кеш успешно сброшен."), messages.SUCCESS)

    reset_cache_action.short_description = ("Сбросить кеш")
