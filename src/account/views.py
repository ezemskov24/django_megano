# from django.contrib.auth import authenticate, login
# from django.http import HttpRequest
# from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.views.generic import TemplateView, DetailView
from django.urls import reverse_lazy
# from django.contrib.auth.forms import UserCreationForm
# from django.views.generic.edit import CreateView

# Login
# class UserLoginView(LoginView):
#     template_name = 'registration/login.jinja2'
#     redirect_authenticated_user = True
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         print(context['form'].as_p())
#         return context


# def UserLoginView(request: HttpRequest):
#     if request.method == "GET":
#         if request.user.is_authenticated:
#             return redirect('/profile/')
#
#         return render(request, 'registration/login.jinja2')
#
#     email = request.POST['email']
#     # username = request.POST['username']
#     password = request.POST['password']
#
#     user = authenticate(request, email=email, password=password)
#     if user is not None:
#         login(request, user)
#         return redirect('/profile/')
#     return render(request, 'registration/login.jinja2', {'error': 'invalid login'})

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from account.models import Seller
from adminsettings.models import SiteSettings
from products.models import Product
from .models import BrowsingHistory


def UserLoginView(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/account/profile/')

        return render(request, 'registration/login.jinja2')

    email = request.POST.get('email')
    password = request.POST.get('pass')

    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return redirect('/account/profile/')

    return render(request, 'registration/login.jinja2', {'error': 'Неверный логин или пароль'})


# Logout
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('account:login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context['form'].as_p())
        return context


class UserProfileView(TemplateView):
    template_name = 'registration/profile.jinja2'


class SellerDetailView(DetailView):
    template_name = 'users/seller_details.jinja2'
    model = Seller
    context_object_name = 'seller'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = Product.objects.filter(sellers=kwargs['object']).order_by('-count_sells')
        context['top_products_cache_time'] = (
            SiteSettings.objects.values('top_product_cache_time')[0]['top_product_cache_time']
        )

        return context


class UserBrowsingHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/browsing-history.jinja2'
    login_url = 'account:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        history = BrowsingHistory.objects.filter(profile=self.request.user).order_by('-timestamp')[:20]

        for item in history:
            product = item.product
            first_image = product.images.first()

            item.image_url = first_image.image.url if first_image else None

        context['history'] = history

        return context
