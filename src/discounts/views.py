from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.views.generic import TemplateView

from .models import ProductDiscount


class DiscountsListView(TemplateView):
    template_name = 'discounts/discounts.jinja2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        discounts = []

        product_discounts = ProductDiscount.objects.filter(active=True)

        discounts.extend(product_discounts)

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
