from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.views.generic import TemplateView, DetailView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    DetailView,
    TemplateView,
    UpdateView,
)

from .forms import ProfileForm, UserRegistrationForm
from .models import BrowsingHistory, Profile, Seller
from adminsettings.models import SiteSettings
from products.models import Product

from .forms import ProfileForm
from django.contrib import messages


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/account/login/'
    model = Profile
    form_class = ProfileForm
    template_name = 'registration/profile.jinja2'
    success_url = reverse_lazy('account:profile')

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     messages.success(self.request, "Данные успешно обновлены.")
    #     return response

    def form_valid(self, form):
        response = super().form_valid(form)

        password1 = form.cleaned_data.get('new_password1')
        password2 = form.cleaned_data.get('new_password2')
        # print('password_view = ', password, '!')
        # # password2 = form.cleaned_data.get('password2')

        if password1 and password1 == password2:
            self.object.set_password(password1)
            # self.object.save()
        # if password:
        #     print('пароль предоставлен!')
        #     self.object.set_password(password)
        #     self.object.save()
        # else:
        #     print('пароль not предоставлен!')
        #
        messages.success(self.request, "Данные успешно обновлены.")
        # else:
        #     raise messages.error(self.request, "Ошибка обновления данных.")
        if self.object.save():
            print("Данные успешно обновлены.")
            messages.success(self.request, "Данные успешно обновлены.")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Ошибка обновления данных.")
        return response

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/registr.jinja2'
    success_url = reverse_lazy('account:account')

    def form_valid(self, form):
        form.save()
        response = super().form_valid(form)

        if form.cleaned_data['password1'] != form.cleaned_data['password2']:
            messages.error(self.request, 'Пароли не совпадают.')
            return self.render_to_response(self.get_context_data(form=form))

        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'registration/login.jinja2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context



# Logout
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('account:login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context['form'].as_p())
        return context


# @login_required(login_url='login')
class UserProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/account/login/'
    template_name = 'registration/profile.jinja2'


class UserAccountView(LoginRequiredMixin, TemplateView):
    login_url = '/account/login/'
    template_name = 'registration/account.jinja2'


class HistoryOrderView(LoginRequiredMixin, TemplateView):
    login_url = '/account/login/'
    template_name = 'registration/historyorder.jinja2'

class UserEmailView(TemplateView):
    template_name = 'registration/e-mail.jinja2'
    # template_name = 'registration/e-mail.jinja2'


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
