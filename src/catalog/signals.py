from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Review


@receiver(post_save, sender=Review)
def clear_review_cache(sender, instance, **kwargs):
    """
    Очистка кеша при добавлении отзыва
    """
    product = instance.product
    cache_key = f'product_details_{product.pk}'
    cache.delete(cache_key)
