from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.urls import reverse
from django.views.generic import TemplateView

from .models import (
    BulkDiscount,
    CategoryDiscount,
    ComboDiscount,
    ProductDiscount,
)


class DiscountsListView(TemplateView):
    template_name = 'discounts/discounts.jinja2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        discounts = []

        product_discounts = ProductDiscount.current.all()
        for discount in product_discounts:
            discount.url = reverse(
                'discounts:products-on-sale',
                kwargs={'sale': discount.slug},
            )
        discounts.extend(product_discounts)

        category_discounts = CategoryDiscount.current.all()
        for discount in category_discounts:
            discount.url = reverse(
                'discounts:products-on-sale',
                kwargs={'sale': discount.slug},
            )
        discounts.extend(category_discounts)

        bulk_discounts = BulkDiscount.current.all()
        for discount in bulk_discounts:
            discount.url = reverse('products:catalog')
        discounts.extend(bulk_discounts)

        combo_discounts = ComboDiscount.current.all()
        for discount in combo_discounts:
            discount.url = reverse(
                'discounts:products-on-sale',
                kwargs={'sale': discount.slug},
            )
        discounts.extend(combo_discounts)

        discounts.sort(key=lambda x: x.end)

        paginator = Paginator(discounts, 12)
        page_number = self.request.GET.get('p', 1)
        try:
            discounts = paginator.page(page_number)
        except PageNotAnInteger:
            discounts = paginator.page(1)
        except EmptyPage:
            discounts = paginator.page(paginator.num_pages)

        context['discounts'] = discounts

        return context
