from django.contrib import admin

from . import models


@admin.register(models.Cart)
class PropertyValueAdmin(admin.ModelAdmin):

    list_display = [
        'product_seller',
        'product_name',
        'count',
    ]
