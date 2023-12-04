from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Seller


class SellersListView(ListView):
    template_name = 'users/sellers_list.html'
    model = Seller
    context_object_name = 'sellers'


class SellerDetailView(DetailView):
    template_name = 'users/seller_details.html'
    model = Seller
    context_object_name = 'seller'
