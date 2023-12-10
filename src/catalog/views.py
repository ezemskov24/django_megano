from django.shortcuts import render

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View

from users.models import Profile
from .forms import ReviewForm
from .models import Review
from .services import add_review, get_count_review, get_reviews_list


def show_review(request: HttpRequest, *args, **kwargs):
    """
    Пример view-функции для внедрения кода страницы для добавленя отзыва к товару.
    """
    context = add_review(request, *args, **kwargs)
    context['count'], context['count_review'] = get_count_review(kwargs['pk'])
    context['reviews_list'] = get_reviews_list(kwargs['pk'])

    return render(request, 'catalog/review_pass.jinja2', context=context)


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