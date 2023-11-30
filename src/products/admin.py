from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from . import admin_filters, models


@admin.action(description="Archive")
def mark_archived(
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        queryset: QuerySet,
):
    queryset.update(archived=True)


@admin.action(description="Un-archive")
def mark_unarchived(
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        queryset: QuerySet,
):
    queryset.update(archived=False)


class PictureInline(admin.StackedInline):
    model = models.Picture
    extra = 1


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [
        mark_archived,
        mark_unarchived
    ]
    inlines = [PictureInline]
    list_display = [
        'name',
        'category',
        'sellers_amount',
        'min_price',
        'avg_price',
        'archived',
    ]
    list_filter = [
        'category',
        'archived',
        admin_filters.MinPriceListFilter,
        admin_filters.AvgPriceListFilter,
    ]
    readonly_fields = ['count_sells']
    search_fields = ['name']

    @admin.display(description='Sellers')
    def sellers_amount(self, obj: models.Product) -> int:
        return obj.sellers.count()

    @admin.display(description='Min price', empty_value=0)
    def min_price(self, obj: models.Product) -> int:
        return obj.min_price()

    @admin.display(description='Avg price', empty_value=0)
    def avg_price(self, obj: models.Product) -> int:
        return obj.average_price()

    def delete_queryset(self, request: HttpRequest, queryset: QuerySet):
        queryset.update(archived=True)


@admin.register(models.SellerProduct)
class SellerProductAdminModel(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    """CategoryAdmin placeholder"""


@admin.register(models.Seller)
class SellerAdmin(admin.ModelAdmin):
    """SellerAdmin placeholder"""
