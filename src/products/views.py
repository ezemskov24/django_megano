from copy import deepcopy

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django_jinja.views.generic import DetailView, ListView, CreateView

from rest_framework.viewsets import ModelViewSet

from .serializer import ProductSerializer, PropertiesSerializer, ValuesSerializer

from .services.compare_products import (add_product_to_compare_list, get_compare_list, get_compare_list_amt,
                                        delete_product_to_compare_list, delete_all_compare_products)

from .banner import Banner
from .models import Product, Property, Value
# from .forms import PropertyNameForm, PropertyCategoryForm

import uuid


def index_view(request: HttpRequest) -> HttpResponse:
    context = {
        'banners': Banner,
    }
    return render(request, 'index.jinja2', context)


def ProductCreateView():
    pass


class ProductDetailsView(DetailView):
    template_name = "products/product_detail.jinja2"
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"

    def post(self, request, *args, **kwargs):
        add_product_to_compare_list(
            request
        )
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
    '''View для отображения страницы сравнения'''
    template_name = 'products/compare_page/compare.jinja2'

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

        context['dif_properties'] = []
        for property_name in context['properties']:
            for property_value in property_name['property_values']:
                if property_value[0].value != property_name['property_values'][0][0].value:
                    context['dif_properties'].append(property_name)
                    break

        return context


def delete_all_compare_products_view(request):
    '''функция ajax запроса для доступа к сервису сравнения'''
    delete_all_compare_products(request)
    return HttpResponse()


def delete_product_to_compare_list_view(request, pk):
    '''функция ajax запроса для доступа к сервису сравнения'''
    delete_product_to_compare_list(request, pk)
    return HttpResponse()


'''
    --------------------------
    вью для  api, пока не используются
    -------------------------
'''


class ProductsCompareViewSet(ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return [
            product[0] for product in [
                Product.objects.filter(pk=pk).select_related('category')
                for pk in get_compare_list(self.request)
                ]
            ]


class PropertiesCompareViewSet(ModelViewSet):
    serializer_class = PropertiesSerializer

    def get_queryset(self):
        pass
