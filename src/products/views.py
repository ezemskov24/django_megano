import random
from typing import Any, Dict

from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.shortcuts import render, get_object_or_404

from .utils import Banner, LimitedProduct, TopSellerProduct
from .banner import Banner
from .models import Product, SellerProduct, Picture


class IndexView(TemplateView):
    template_name = 'index.jinja2'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['banners'] = Banner()
        context['top_sellers'] = TopSellerProduct.get_top_sellers()
        context['limited_offers'] = LimitedProduct.get_limited_offers()

        return context


def ProductCreateView():
    pass


class ProductDetailsView(DetailView):
    template_name = "products/product-details.jinja2"
    model = Product

    def get_context_data(self, **kwargs):
        """
        Получение контекстных данных для представления деталей продукта
        """
        cache_key = f'product_details_{self.object.pk}'
        context_data = cache.get(cache_key)

        if context_data is None:
            product = self.object
            sellers = SellerProduct.objects.filter(product=product).select_related('seller')
            images = Picture.objects.filter(product=product)

            context_data = {
                'product': product,
                'sellers': sellers,
                'images': images
            }

            cache.set(cache_key, context_data, 60 * 60 * 24)

        return context_data


def ProductsListView():
    pass


def ProductUpdateView():
    pass