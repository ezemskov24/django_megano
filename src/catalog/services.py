from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ..users.models import Profile
from .forms import ReviewForm
from .models import Review
from ..products.models import Product


def get_reviews_list(pk: int):
    return Product.objects.get(pk=pk).reviews.all()


def add_review(request: HttpRequest, *args, **kwargs):
    """
    Сервис добавления отзывов к товару.

    Returns:
        context: параметны для отрисовки шаблона, содержит:
            review_template: название шаблона добавления отзыва к товару для имрорта в шаблон страницы товара;
            form: форма для добавления отзыва.
    """
    product = Product.objects.get(pk=kwargs['pk'])
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = Review.objects.create(
                text=form.cleaned_data['text'],
                author=Profile.objects.get(pk=request.user.id),
            )
            product.review.add(review)
            product.save()
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'review_template': 'catalog/review.jinja2',
    }
    return context


def get_count_review(pk: int) -> str:
    """
    Функция для определения количества отзывов на товар.

    Args:
        pk (int): уникальный код товара.

    return:
        result (str) - количество отзывов на товар.
    """
    count_review = len(Product.objects.get(pk=pk).values('reviews')['reviews'])
    if (count_review % 10 == 1) and (count_review % 100 != 11):
        result = f'{count_review} отзыв'
    elif ((count_review % 10 >= 2)
          and (count_review % 10 <= 4)
          and ((count_review % 100 < 10) or (count_review % 100 >= 20))):
        result = f'{count_review} отзыва'
    else:
        result = f'{count_review} отзывов'

    return result
