from enum import Enum
from typing import Any, Dict

from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.db.models import Count, Min
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, TemplateView

from .models import Category, Product, Tag
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

    tag = None
    category = None

    class SortEnum(Enum):
        POP_ASC = '-pop'
        POP_DEC = 'pop'
        PRI_ASC = '-pri'
        PRI_DEC = 'pri'
        REV_ASC = '-rev'
        REV_DEC = 'rev'
        CRE_ASC = '-cre'
        CRE_DEC = 'cre'
        NONE = 'none'

    def get_queryset(self):
        sort = self.request.GET.get('sort')
        if sort:
            if (sort == self.SortEnum.NONE.value and
                    self.request.session.get('sort')):
                del self.request.session['sort']
            else:
                self.request.session['sort'] = sort
        sort = self.request.session.get('sort')

        filter_params = {}
        if self.tag:
            filter_params['tags'] = self.tag
        if self.category:
            categories = [self.category]
            categories.extend([cat for cat in self.category.subcategories.all()])
            filter_params['category__in'] = categories
        if filter_params:
            products_list = Product.active.filter(**filter_params).all()
        else:
            products_list = Product.active.all()

        if sort:
            products_list = self.get_sorted_queryset(products_list, sort)
        paginator = Paginator(products_list, 8)
        page_number = self.request.GET.get('p', 1)
        try:
            products = paginator.page(page_number)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return products

    def get_sorted_queryset(self, queryset, sort):
        if sort == self.SortEnum.CRE_ASC.value:
            return queryset.order_by('created_at').all()
        if sort == self.SortEnum.CRE_DEC.value:
            return queryset.order_by('-created_at').all()
        if sort == self.SortEnum.POP_ASC.value:
            return queryset.order_by('-count_sells').all()
        if sort == self.SortEnum.POP_DEC.value:
            return queryset.order_by('count_sells').all()
        if sort == self.SortEnum.PRI_ASC.value:
            return queryset.annotate(
                price=Min('sellerproduct__price')
            ).order_by('-price').all()
        if sort == self.SortEnum.PRI_DEC.value:
            return queryset.annotate(
                price=Min('sellerproduct__price')
            ).order_by('price').all()
        # Обёрнуто в try-except, чтобы избегать исключений, пока не будут готовы обзоры
        try:
            if sort == self.SortEnum.REV_ASC.value:
                return queryset.annotate(
                    rev_count=Count('reviews')
                ).order_by('-rev_count').all()
            if sort == self.SortEnum.REV_DEC.value:
                return queryset.annotate(
                    rev_count=Count('reviews')
                ).order_by('rev_count').all()
        except:
            pass
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.SortEnum
        curr_sort = self.request.session.get('sort')
        if curr_sort:
            context['curr_sort'] = curr_sort
        context['tags'] = Tag.objects.annotate(
            prod_count=Count('products')
        ).order_by('-prod_count').all()[:10]
        return context

    def get(self, request, *args, **kwargs):
        tag_slug = kwargs.get('tag')
        if tag_slug:
            self.tag = Tag.objects.filter(slug=tag_slug).first()
        category_slug = kwargs.get('category')
        if category_slug:
            self.category = Category.objects.filter(slug=category_slug).first()
        return super().get(request, *args, **kwargs)


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