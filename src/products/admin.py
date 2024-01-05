from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from . import admin_filters, models


@admin.action(description="Archive selected products")
def mark_archived(
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        queryset: QuerySet,
):
    queryset.update(archived=True)


@admin.action(description="Un-archive selected products")
def mark_unarchived(
        modeladmin: admin.ModelAdmin,
        request: HttpRequest,
        queryset: QuerySet,
):
    queryset.update(archived=False)


class PictureInline(admin.StackedInline):
    model = models.Picture
    extra = 1


class SellerInline(admin.TabularInline):
    model = models.SellerProduct
    extra = 1


@admin.register(models.Value)
class PropertyValueAdmin(admin.ModelAdmin):

    actions = [
        mark_archived,
        mark_unarchived
    ]
    list_display = [
        'product',
        'property',
        'value',
    ]


@admin.register(models.Property)
class PropertyAdmin(admin.ModelAdmin):

    actions = [
        mark_archived,
        mark_unarchived
    ]
    list_display = [
        'category',
        'name',
    ]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [
        mark_archived,
        mark_unarchived
    ]
    inlines = [PictureInline, SellerInline]
    list_display = [
        'name',
        'category',
        'sellers_amount',
        'min_price',
        'avg_price',
        'avg_disc_price',
        'sort_index',
        'limited',
        'archived',
    ]
    list_filter = [
        'category',
        'limited',
        'archived',
        admin_filters.MinPriceListFilter,
        admin_filters.AvgPriceListFilter,
    ]
    prepopulated_fields = {
        'slug': ('name',),
    }
    readonly_fields = ['count_sells']
    search_fields = ['name']

    @admin.display(description='Sellers')
    def sellers_amount(self, obj: models.Product) -> int:
        return obj.sellers.count()

    @admin.display(description='Min price', empty_value=0)
    def min_price(self, obj: models.Product) -> int:
        return obj.min_price

    @admin.display(description='Avg price', empty_value=0)
    def avg_price(self, obj: models.Product) -> int:
        return obj.average_price

    @admin.display(description='Avg disc price', empty_value=0)
    def avg_disc_price(self, obj: models.Product) -> int:
        return obj.discounted_average_price

    def delete_queryset(self, request: HttpRequest, queryset: QuerySet):
        queryset.update(archived=True)


@admin.register(models.SellerProduct)
class SellerProductAdminModel(admin.ModelAdmin):
    pass


class SubcategoryInline(admin.TabularInline):
    model = models.Category
    extra = 0
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'parent_category',
        'is_active',
        'sort_index',
    ]
    prepopulated_fields = {
        'slug': ('name',),
    }
    search_fields = ['name']
    list_filter = ['is_active']
    list_editable = ['is_active', 'sort_index']
    inlines = [SubcategoryInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent_category":
            kwargs["queryset"] = models.Category.objects.filter(
                parent_category=None,
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ]
    prepopulated_fields = {
        'slug': ('name',),
    }
