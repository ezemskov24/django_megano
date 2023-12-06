from django.db import models


class Product(models.Model):
    """
    Заглушка класса для описания товаров.
    """


class Category(models.Model):
    """
    Класс категорий товаров
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    parent_category = models.ForeignKey('self', null=True, blank=True, related_name='children',
                                        on_delete=models.CASCADE)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    icon = models.ImageField(upload_to='category_icons/', null=True, blank=True)
    sort_index = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_index', 'name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name



