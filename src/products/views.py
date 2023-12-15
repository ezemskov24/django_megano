from copy import deepcopy

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django_jinja.views.generic import DetailView, ListView, CreateView

from .services.compare_products import (add_product_to_compare_list, get_compare_list, get_compare_list_amt,
                                        delete_product_to_compare_list, delete_all_compare_products)

from .banner import Banner
from .models import Product, Property, Value
from .forms import PropertyNameForm, PropertyCategoryForm

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
        print(get_compare_list(request))
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


# class PropertyCreateView(CreateView):
#     template_name = 'products/create_property.jinja2'
#     model = Property
#     fields = '__all__'
#
#     def get_form(self, form_class=None, fields_amt=None):
#         if fields_amt:
#             form_class = PropertyNameForm(fields_amt)
#             return form_class
#         form_class = PropertyCategoryForm()
#         return form_class
#
#     def post(self, request, *args, **kwargs):
#         context = dict()
#         print(request.POST)
#         if request.POST.get('names_amt'):
#             form = self.get_form(fields_amt=int(request.POST.get('names_amt')))
#             context['form'] = form
#             return render(request, 'products/create_property.jinja2', context=context)
#
#         fields_dict = deepcopy(request.POST)
#         fields_dict.pop('csrfmiddlewaretoken')
#
#         for key, value in fields_dict.items():
#             fields_dict[key] = value[0]
#         print(fields_dict)
#         # Property.object.bulk_create(
#         # )
#         return HttpResponseRedirect(reverse('products:create'))

        # context = dict()
        # if request.POST.get('fields_amt'):
        #
        #     fields_amt = int(request.POST.get('fields_amt'))
        #     # context['form'] = form
        #     context = self.get_context_data()
        #
        #     return render(request, 'products/create_property.jinja2', context=context)
        # if request.POST.get('create'):
        #     # form = PropertyCategoryForm
        #     # print(form)
        #     # context['form'] = form
        #     # fields_dict = deepcopy(request.POST)
        #     # fields_dict.pop('csrfmiddlewaretoken')
        #     # fields_dict.pop('create')
        #     # print(fields_dict)
        #     # for key, value in fields_dict.items():
        #     #     fields_dict[key] = value[0]
        #
        #     # Property.object.bulk_create(
        #     #
        #     # )
        #     return HttpResponseRedirect(reverse('products:create'))

