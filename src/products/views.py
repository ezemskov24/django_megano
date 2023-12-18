from enum import Enum
from typing import Any, Dict

from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.db.models import Count, Max, Min, Sum
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, TemplateView

from .forms import FilterForm
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

    QS_KEY = 'catalog_queryset'
    FP_KEY = 'catalog_filter_price'

    def __init__(self):
        super().__init__()
        self.tag = None
        self.categories = None
        self.filter_params = {}
        self.filter_prices = {}
        self.filter_name = None
        self.filter_in_stock = None

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
        products_list = self._get_base_queryset()
        products_list = self._get_filtered_queryset(products_list)
        sort = self._get_selected_sort_type()
        products_list = self._get_sorted_queryset(products_list, sort)

        paginator = Paginator(products_list, 8)
        page_number = self.request.GET.get('p', 1)
        try:
            products = paginator.page(page_number)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return products

    def _get_base_queryset(self):
        if self.tag or self.categories:
            base_filter = {}
            if self.tag:
                base_filter['tags'] = self.tag
            if self.categories:
                base_filter['category__in'] = self.categories

            products_list = Product.active.filter(**base_filter)
        else:
            products_list = Product.active

        prices = products_list.aggregate(
            min=Min('sellerproduct__price'),
            max=Max('sellerproduct__price'),
        )
        self.filter_prices['min'] = str(prices['min'])
        self.filter_prices['max'] = str(prices['max'])
        if not self.filter_prices.get('selected_min'):
            self.filter_prices['selected_min'] = str(prices['min'])
        if not self.filter_prices.get('selected_max'):
            self.filter_prices['selected_max'] = str(prices['max'])

        return products_list

    def _get_filtered_queryset(self, queryset):
        if self.filter_params:
            if 'amount__gt' or 'price__lte' in self.filter_params:
                queryset = queryset.annotate(
                    amount=Sum('sellerproduct__count'),
                    price=Min('sellerproduct__price'),
                ).filter(**self.filter_params)
            else:
                queryset = queryset.filter(**self.filter_params)
        return queryset

    def _get_selected_sort_type(self):
        sort = self.request.GET.get('sort')
        if sort:
            if (sort == self.SortEnum.NONE.value and
                    self.request.session.get('sort')):
                del self.request.session['sort']
            else:
                self.request.session['sort'] = sort
        sort = self.request.session.get('sort')
        if not sort:
            sort = self.SortEnum.NONE.value
        return sort

    def _get_sorted_queryset(self, queryset, sort):
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

        return queryset.order_by('sort_index').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = self.SortEnum
        curr_sort = self.request.session.get('sort')
        if curr_sort:
            context['curr_sort'] = curr_sort
        context['tags'] = Tag.objects.annotate(
            prod_count=Count('products')
        ).order_by('-prod_count').all()[:10]

        widget_attrs = FilterForm.declared_fields['price'].widget.attrs
        widget_attrs['data-min'] = self.filter_prices['min']
        widget_attrs['data-max'] = self.filter_prices['max']
        widget_attrs['data-from'] = self.filter_prices['selected_min']
        widget_attrs['data-to'] = self.filter_prices['selected_max']

        FilterForm.declared_fields['title'].widget.attrs['value'] = (
            self.filter_name
        ) if self.filter_name else ''
        FilterForm.declared_fields['in_stock'].widget.attrs['checked'] = (
            True
        ) if self.filter_in_stock else False

        context['filter_form'] = FilterForm()

        return context

    def get(self, request, *args, **kwargs):
        self._get_path_params(**kwargs)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self._get_path_params(**kwargs)
        filter_form = FilterForm(request.POST)
        if filter_form.is_valid():
            cd = filter_form.cleaned_data
            if cd['price']:
                price = cd['price'].split(';')
                self.filter_params['price__gte'] = price[0]
                self.filter_params['price__lte'] = price[1]
                self.filter_prices['selected_min'] = price[0]
                self.filter_prices['selected_max'] = price[1]
            if cd['title']:
                self.filter_params['name__icontains'] = cd['title']
                self.filter_name = cd['title']
            if cd['in_stock']:
                self.filter_params['amount__gt'] = 0
                self.filter_in_stock = True

        return self.get(request, args, kwargs)

    def _get_path_params(self, **kwargs):
        tag_slug = kwargs.get('tag')
        if tag_slug:
            tag = Tag.objects.filter(slug=tag_slug).first()
            if tag:
                self.tag = tag.pk

        category_slug = kwargs.get('category')
        if category_slug:
            category = Category.objects.filter(slug=category_slug).first()
            if category:
                categories = [category.pk]
                categories.extend(
                    [cat.pk for cat in category.subcategories.all()]
                )
                self.categories = categories


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