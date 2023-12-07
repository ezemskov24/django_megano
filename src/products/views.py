from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .banner import Banner


def index_view(request: HttpRequest) -> HttpResponse:
    context = {
        'banners': Banner(),
    }
    return render(request, 'index.jinja2', context)


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