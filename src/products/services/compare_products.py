from django.http import HttpRequest

from django.core.cache import cache

from ..models import Product


session_key = 'compare_list_key'
max_list_amt = 4


def delete_product_to_compare_list(request, pk):
    '''убирает товар из списка сравнения'''
    compare_list = request.session.get(session_key, [])
    compare_list.remove(str(pk))
    request.session[session_key] = compare_list
    return


def get_compare_list(request, product_amt=max_list_amt):
    '''
    Возвращает список товаров из списка сравнения
    (по умолчанию первые 3 товара)
    '''
    return request.session.get(session_key, [])[:product_amt]


def get_compare_list_amt(request):
    '''возвращает количество товаров в списке сравнения'''
    return len(get_compare_list(request))


def add_product_to_compare_list(request):
    '''добавляет товар в список сравнения'''
    compare_list = request.session.get(session_key, [])
    product_id = request.POST.get('product_to_compare')
    if product_id in compare_list or get_compare_list_amt(request) == max_list_amt:
        return
    compare_list.append(product_id)
    request.session[session_key] = compare_list
    return


def delete_all_compare_products(request):
    request.session[session_key] = []
    return
