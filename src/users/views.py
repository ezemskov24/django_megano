from django.shortcuts import render
from django.views.generic import DetailView

from .models import Seller


class SellerDetailView(DetailView):
    template_name = 'users/seller_details.jinja2'
    model = Seller
    context_object_name = 'seller'
