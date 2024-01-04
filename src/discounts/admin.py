from django.contrib import admin

from .models import BulkDiscount, CategoryDiscount, ProductDiscount


@admin.register(ProductDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'weight',
        'start',
        'end',
        'active',
    ]
    list_editable = [
        'weight',
    ]
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(CategoryDiscount)
class CategoryDiscountAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'weight',
        'start',
        'end',
        'active',
    ]
    list_editable = [
        'weight',
    ]
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(BulkDiscount)
class BulkCategoryDiscount(admin.ModelAdmin):
    list_display = [
        'name',
        'weight',
        'start',
        'end',
        'active',
    ]
    list_editable = [
        'weight',
    ]
    prepopulated_fields = {
        'slug': ('name',),
    }
