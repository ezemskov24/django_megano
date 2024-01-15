from django.shortcuts import render

from django.http import HttpRequest

from .forms import ReviewForm
from .services import add_review, get_count_review, get_reviews_list


# def show_review(request: HttpRequest, *args, **kwargs):
#     """
#     Пример view-функции для внедрения кода страницы для добавленя отзыва к товару.
#     """
#     form = ReviewForm(kwargs['post'])
#     if form.is_valid():
#         context = add_review(text=request.POST['text'], user_id=request.user.id, **kwargs)
#     else:
#         context = {}
#
#     context['form'] = form
#     context['count'], context['count_review'] = get_count_review(kwargs['pk'])
#     context['reviews_list'] = get_reviews_list(kwargs['pk'])
#
#     return render(request, 'catalog/review_pass.jinja2', context=context)


def add_to_comparison(request, product_id):
    # добавить продукт для сравнения
    return None

def remove_from_comparison(request, product_id):
    # удалить продукт из сравнения
    return None

def comparison_list(request):
    # список сравниваемых продуктов
    return None

def comparison_count(request):
    # количество товаров в списке сравнения
    return None