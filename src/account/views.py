from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView

from .forms import UserRegistrationForm #, ProfileUpdateForm
from .models import Profile

from .models import Seller
from adminsettings.models import SiteSettings
from products.models import Product

from .forms import ProfileForm
from django.contrib import messages


# @method_decorator(login_required(login_url='../login'), name='dispatch')
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/account/login/'
    model = Profile
    form_class = ProfileForm
    template_name = 'registration/profile.jinja2'
    success_url = reverse_lazy('account:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        # messages.success(self.request, "Data updated.")
        messages.success(self.request, "Данные успешно обновлены.")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        # messages.error(self.request, "Data not updated.")
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
        return redirect('/account/account/')

    return render(request, 'registration/login.jinja2', {'error': 'Неверный логин или пароль'})


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


# @login_required(login_url='login')
# @method_decorator(login_required(login_url='../login'), name='dispatch')
class UserAccountView(LoginRequiredMixin, TemplateView):
    login_url = '/account/login/'
    template_name = 'registration/account.jinja2'


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
