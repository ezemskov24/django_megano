from rest_framework import serializers

from products.models import SellerProduct
from cart.models import Cart, Order


class ProductSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProduct
        fields = (
            'pk',
            'product',
            'seller',
            'count',
            'price',
        )


class CartSerializer(serializers.ModelSerializer):
    product_seller = ProductSellerSerializer()

    class Meta:
        model = Cart
        fields = (
            'pk',
            'product_seller',
            'profile',
            'count',
        )


class CartPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = (
            'pk',
            'product_seller',
            'profile',
            'count',
        )


# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cart
#         fields = (
#             'product_seller.product',
#             'product_seller.product.name',
#             'product_seller.price',
#             'count',
#         )


