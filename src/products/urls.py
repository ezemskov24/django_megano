from django.urls import path

from . import views

app_name = "products"

urlpatterns = [

    path(
        "products/<slug:slug>/",
        views.ProductDetailsView.as_view(),
        name="product_details",
    ),
    path(
        'compare/',
        views.ProductsCompareView.as_view(),
        name='product_compare',
    ),
    path('t/<slug:tag>', views.CatalogView.as_view(), name='products-by-tag'),
    path(
        'category/<slug:category>',
        views.CatalogView.as_view(),
        name='products-by-category'
    ),
    path('', views.CatalogView.as_view(), name='catalog'),
    # path("products/<int:pk>/update/", ProductUpdateView, name="product_update"),
    # path("products/", ProductsListView, name="products_list"),
    # path("products/create/", ProductCreateView, name="product_create"),
]
