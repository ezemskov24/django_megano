from enum import Enum
from typing import Any, Dict

from django.db.models import QuerySet, Count, Min, Max, Sum, BooleanField, ExpressionWrapper, Q
from django.http import HttpRequest

from ..forms import FilterForm, SearchForm
from ..models import Product, Tag, Category
from discounts.models import CategoryDiscount, ComboDiscount, ProductDiscount


class SortEnum(Enum):
    """ Перечисление параметров сортировки товаров. """
    POP_ASC = '-pop'
    POP_DEC = 'pop'
    PRI_ASC = '-pri'
    PRI_DEC = 'pri'
    REV_ASC = '-rev'
    REV_DEC = 'rev'
    CRE_ASC = '-cre'
    CRE_DEC = 'cre'
    NONE = 'none'


class CatalogQuerySetProcessor:
    def __init__(self):
        self.tag = None
        self.categories = None
        self.products = None
        self.filter_params = {}
        self.filter_prices = {}
        self.filter_name = None
        self.filter_in_stock = None
        self.search_query = None

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        products_list = self._get_base_queryset(request)
        products_list = self._get_filtered_queryset(products_list)
        sort = self._get_selected_sort_type(request)
        products_list = self._get_sorted_queryset(products_list, sort)

        return products_list

    def _get_base_queryset(self, request) -> QuerySet:
        """ Получение базового queryset для дальнейшей работы. """
        search_query = request.session.get('search_query')
        # base_filter = {'seller_count__gt': 0}
        base_filter = {}
        if self.tag or self.categories or self.products or search_query:
            if self.tag:
                base_filter['tags'] = self.tag
            if self.categories:
                base_filter['category__in'] = self.categories
            if self.products:
                base_filter['pk__in'] = self.products
            if search_query:
                base_filter['name__icontains'] = search_query

        products_list = Product.active.annotate(
            seller_count=Count('sellerproduct'),
        ).filter(**base_filter)

        prices = products_list.aggregate(
            min=Min('sellerproduct__price'),
            max=Max('sellerproduct__price'),
        )
        min_pr = prices['min']
        if not min_pr:
            min_pr = 0
        max_pr = prices['max']
        if not max_pr:
            max_pr = 0

        self.filter_prices['min'] = str(min_pr)
        self.filter_prices['max'] = str(max_pr)
        if not self.filter_prices.get('selected_min'):
            self.filter_prices['selected_min'] = str(min_pr)
        if not self.filter_prices.get('selected_max'):
            self.filter_prices['selected_max'] = str(max_pr)

        return products_list

    def _get_filtered_queryset(self, queryset: QuerySet) -> QuerySet:
        """
        Получение отфильтрованного queryset.

        Args:
            - queryset: queryset, подлежащий фильтрованию.
        """
        if self.filter_params:
            if 'amount__gt' or 'price__lte' in self.filter_params:
                queryset = queryset.annotate(
                    amount=Sum('sellerproduct__count'),
                    price=Min('sellerproduct__price'),
                ).filter(**self.filter_params)
            else:
                queryset = queryset.filter(**self.filter_params)
        return queryset

    @staticmethod
    def _get_selected_sort_type(request: HttpRequest) -> str:
        """ Получение выбранного типа сортировки из запроса. """
        sort = request.GET.get('sort')
        if sort:
            if (sort == SortEnum.NONE.value and
                    request.session.get('sort')):
                del request.session['sort']
            else:
                request.session['sort'] = sort
        sort = request.session.get('sort')
        if not sort:
            sort = SortEnum.NONE.value
        return sort

    @staticmethod
    def _get_sorted_queryset(queryset: QuerySet, sort: str) -> QuerySet:
        """
        Получение отсортированного queryset.

        Args:
            - queryset: queryset, подлежащего сортировке.
            - sort: тип сортировки.
        """
        annotate_params = {
            'in_stock': ExpressionWrapper(
                Q(seller_count__gt=0),
                output_field=BooleanField()
            )
        }
        sort_params = ['-in_stock']
        if sort == SortEnum.CRE_ASC.value:
            sort_params.append('created_at')

        if sort == SortEnum.CRE_DEC.value:
            sort_params.append('-created_at')

        if sort == SortEnum.POP_ASC.value:
            sort_params.append('-count_sells')

        if sort == SortEnum.POP_DEC.value:
            sort_params.append('count_sells')

        if sort == SortEnum.PRI_ASC.value:
            annotate_params['price'] = Min('sellerproduct__price')
            sort_params.append('-price')

        if sort == SortEnum.PRI_DEC.value:
            annotate_params['price'] = Min('sellerproduct__price')
            sort_params.append('price')

        if sort == SortEnum.REV_ASC.value:
            annotate_params['rev_count'] = Count('reviews')
            sort_params.append('-rev_count')

        if sort == SortEnum.REV_DEC.value:
            annotate_params['rev_count'] = Count('reviews')
            sort_params.append('rev_count')

        sort_params.append('sort_index')
        return queryset.annotate(
            **annotate_params,
        ).order_by(*sort_params).all()

    def get_context_data(
            self,
            context: Dict[str, Any],
            request: HttpRequest,
    ) -> Dict[str, Any]:
        context['sort'] = SortEnum
        curr_sort = request.session.get('sort')
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

    def process_get_params(self, request: HttpRequest, **kwargs):
        self._process_path_params(**kwargs)
        print(1)
        if self.filter_params:
            print(2)
            request.session['filter_params'] = self.filter_params
        else:
            filter_params = request.session.get('filter_params')
            if filter_params:
                if not request.GET.get('p'):
                    print(3)
                    del request.session['filter_params']
                else:
                    print(4)
                    self.filter_params = filter_params

        if self.search_query:
            request.session['search_query'] = self.search_query
        elif (
                request.session.get('search_query')
                and not request.GET.get('p')
                and not self.filter_params
        ):
            del request.session['search_query']

    def process_post_params(self, request: HttpRequest, **kwargs):
        self._process_path_params(**kwargs)
        filter_form = FilterForm(request.POST)
        search_form = SearchForm(request.POST)
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
                self.filter_params['seller_count__gt'] = 0
                self.filter_in_stock = True

        if search_form.is_valid():
            self.search_query = search_form.cleaned_data['query']

    def _process_path_params(self, **kwargs):
        """ Обработка параметров из пути запроса. """
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

        discount_slug = kwargs.get('sale')
        if discount_slug:
            self._process_discount_slug(discount_slug)

    def _process_discount_slug(self, discount_slug: str):
        product_discount = ProductDiscount.current.filter(
                slug=discount_slug,
            ).prefetch_related('products').first()

        category_discount = CategoryDiscount.current.filter(
                slug=discount_slug,
            ).prefetch_related('categories').first()

        combo_discount = ComboDiscount.current.filter(
            slug=discount_slug,
        ).prefetch_related('set_1', 'set_2').first()

        products = []
        categories = []

        if product_discount:
            products = list(
                product_discount.products.values_list('pk', flat=True).all(),
            )

        if category_discount:
            categories = list(
                category_discount.categories.values_list('pk', flat=True).all(),
            )

        if combo_discount:
            products.extend(
                list(
                    combo_discount.set_1.products.values_list(
                        'pk',
                        flat=True,
                    ).all(),
                ),
            )
            products.extend(
                list(
                    combo_discount.set_2.products.values_list(
                        'pk',
                        flat=True,
                    ).all(),
                ),
            )
            categories.extend(
                list(
                    combo_discount.set_1.categories.values_list(
                        'pk',
                        flat=True,
                    ).all(),
                ),
            )
            categories.extend(
                list(
                    combo_discount.set_2.categories.values_list(
                        'pk',
                        flat=True,
                    ).all(),
                ),
            )

        if products:
            self.products = products
        if categories:
            self.categories = categories
