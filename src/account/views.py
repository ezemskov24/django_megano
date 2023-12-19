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


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'registration/profile.jinja2'
    success_url = reverse_lazy('account:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('Form is_valid(self) = ', context['form'].is_valid())
        print('*'*8, '\ncontext ', context['form'])
        print('*'*8)


        return context

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/registr.jinja2'
    success_url = reverse_lazy('account:account')

    def form_valid(self, form):
        form.save()
        response = super().form_valid(form)

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


class UserAccountView(TemplateView):
    template_name = 'registration/account.jinja2'

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
