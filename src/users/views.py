from django.shortcuts import render
from django.views.generic import DetailView

from products.models import SellerProduct, Product
from adminsettings.models import SiteSettings
from .models import Seller


class SellerDetailView(DetailView):
    template_name = 'users/seller_details.jinja2'
    model = Seller
    context_object_name = 'seller'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = Product.objects.filter(sellers=kwargs['object']).values(
            'name',
            'description',
            'count_sells',
            'images__image',
            'sellerproduct__price',
            'sellerproduct__count',
        ).order_by('-count_sells')
        print('time=', SiteSettings.objects.values('top_product_cache_time')[0]['top_product_cache_time'])
        context['top_products_cache_time'] = (
            SiteSettings.objects.values('top_product_cache_time')[0]['top_product_cache_time']
        )
        return context
