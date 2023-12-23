from rest_framework import serializers

from .models import Product, Property, Value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'category',
            'name',
            'slug',
            'description',
            'manufacturer',
            'created_at',
            'count_sells',
            'archived',
        )


class PropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            'category',
            'name',
        )


class ValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            'product',
            'property',
            'value',
        )
