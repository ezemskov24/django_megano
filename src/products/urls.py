from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path('', views.CatalogView.as_view(), name='catalog'),
    path('t/<slug:tag>', views.CatalogView.as_view(), name='products-by-tag'),
    path(
        'category/<slug:category>',
        views.CatalogView.as_view(),
        name='products-by-category'
    ),
    # path("products/", ProductsListView, name="products_list"),
    # path("products/create/", ProductCreateView, name="product_create"),
    # path("products/<int:pk>/", ProductDetailsView, name="product_details"),
    # path("products/<int:pk>/update/", ProductUpdateView, name="product_update"),
]
