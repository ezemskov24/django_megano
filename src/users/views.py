from django.shortcuts import render
from django.views.generic import DetailView

from .models import Seller, CountProduct


class SellerDetailView(DetailView):
    template_name = 'users/seller_details.jinja2'
    model = Seller
    context_object_name = 'seller'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print('id=', self)
    #     queryset = CountProduct.objects.filter(seller=1).order_by()
    #     print("queryset=", queryset.__dict__)
    #     # context['products'] = queryset
    #     # print(context)
    #     return context
