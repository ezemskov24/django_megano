from rest_framework.serializers import ModelSerializer

from products.models import Product
from products.models import SellerProduct
from cart.models import Cart


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'slug',
            'description',
        )


class ProductSellerSerializer(ModelSerializer):
    # product = ProductSerializer()

    class Meta:
        model = SellerProduct
        fields = (
            'product',
            'seller',
            'count',
            'price',
        )


class CartSerializer(ModelSerializer):
    product_seller = ProductSellerSerializer()

    class Meta:
        model = Cart
        fields = (
            'pk',
            'product_name',
            'product_seller',
            'profile',
            'count',
        )
