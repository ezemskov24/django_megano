from django.contrib import admin

from . import models


@admin.register(models.ProductDiscount)
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


@admin.register(models.CategoryDiscount)
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


@admin.register(models.BulkDiscount)
class BulkCategoryDiscountAdmin(admin.ModelAdmin):
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


@admin.register(models.ComboDiscount)
class ComboDiscountAdmin(admin.ModelAdmin):
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


@admin.register(models.ComboSet)
class ComboSetAdmin(admin.ModelAdmin):
    pass