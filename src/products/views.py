from typing import Any, Dict

from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, ListView
from django.utils import timezone

from catalog.forms import ReviewForm
from catalog.services import get_reviews_list, add_review, get_count_review
from .services.compare_products import add_product_to_compare_list, get_compare_list, delete_all_compare_products, \
    delete_product_to_compare_list
from .utils import Banner, LimitedProduct, TopSellerProduct
from .models import Product, SellerProduct, Picture
from catalog.models import Review
from account.models import BrowsingHistory


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
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user.is_authenticated:
            browsing_history, created = BrowsingHistory.objects.get_or_create(
                profile=request.user, product=self.object
            )

            if not created:
                browsing_history.timestamp = timezone.now()
                browsing_history.save()

        context_data = self.get_context_data()

        return self.render_to_response(context_data)

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
            reviews = Review.objects.filter(product=product).order_by('-created_at')

            context_data = {
                'product': product,
                'sellers': sellers,
                'images': images,
                'reviews': reviews,
                'reviews_list': get_reviews_list(product.pk),
                'get_count_review': get_count_review(product.pk)
            }

            cache.set(cache_key, context_data, 60 * 60 * 24)

        return context_data

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)

        if form.is_valid():
            add_review(post=request.POST, user_id=request.user.id, pk=kwargs['pk'])

            return redirect('products:product_details', pk=kwargs['pk'])

        add_product_to_compare_list(request)
        return HttpResponseRedirect(
            reverse('products:product_details',
                    kwargs={'pk': kwargs.get('pk')}
                    )
        )


def ProductsListView():
    pass


def ProductUpdateView():
    pass


class ProductsCompareView(ListView):
    template_name = 'products/compare.jinja2'

    def get_queryset(self):
        return [
            product[0] for product in [
                Product.objects.filter(pk=pk).select_related('category')
                for pk in get_compare_list(self.request)
                ]
            ]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        if not context['object_list']:
            return context

        for product in context.get('object_list'):
            context['properties'] = [
                {
                    'property_name': value.property
                }
                for value in product.product_property_value.select_related('property')
            ]

        for property_name in context['properties']:
            property_name['property_values'] = [
                property_name['property_name'].category_property_value.filter(product=product)
                for product in context.get('object_list')
            ]

        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('product_from_compare') == 'delete':
            delete_all_compare_products(request)
            return HttpResponseRedirect(reverse('products:product_compare'))
        delete_product_to_compare_list(request)
        return HttpResponseRedirect(reverse('products:product_compare'))
