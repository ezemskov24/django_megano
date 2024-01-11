from django.contrib import admin

from cart.models import Order, Cart


# class OrderInLine(admin.TabularInline):
#     model = Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'profile', 'fio', 'phone', 'email', \
                   'city', 'delivery_address', 'delivery_type', \
                   'payment_type', 'comment', 'archived', 'created_at'
    ordering = 'created_at',
    # inlines = [
    #         OrderInLine,
    #     ]

    def get_queryset(self, request):
        return Order.objects.select_related("cart")
