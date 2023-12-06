from django.shortcuts import render

from django.http import HttpRequest, HttpResponse

from users.models import Profile
from .forms import ReviewForm
from .models import Review
from .services import add_review


def show_review(request: HttpRequest):
    """
    Пример view-функции для внедрения кода страницы для добавленя отзыва к товару.
    """
    context = add_review(request)
    print(context)
    return render(request, 'catalog/review_pass.jinja2', context=context)
