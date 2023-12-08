from django.db import models
from account.models import Profile


class Review(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    text = models.TextField(max_length=1000, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
