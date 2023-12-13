from typing import Any, Dict

from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, TemplateView

from .models import Product
from .utils import Banner, LimitedProduct, TopSellerProduct


class IndexView(TemplateView):
    template_name = 'index.jinja2'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['banners'] = Banner()
        context['top_sellers'] = TopSellerProduct.get_top_sellers()
        context['limited_offers'] = LimitedProduct.get_limited_offers()

        return context


class CatalogView(ListView):
    template_name = 'catalog/catalog.jinja2'
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        products_list = Product.active.all()
        paginator = Paginator(products_list, 8)
        page_number = self.request.GET.get('p', 1)
        try:
            products = paginator.page(page_number)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return products


def ProductCreateView():
    pass


def ProductDetailsView(DetailView):
    template_name = "shopapp/products-details.html"
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


def ProductsListView():
    pass


def ProductUpdateView():
    pass