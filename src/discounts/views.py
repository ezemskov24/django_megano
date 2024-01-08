from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.urls import reverse
from django.views.generic import TemplateView

from .services.discount_list import get_discounts
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
        discounts = get_discounts()

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
