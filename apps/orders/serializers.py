from rest_framework import serializers
from .models import Basket, OrderItem, Order


class BasketSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='color.product.name_uz', read_only=True)
    color_name = serializers.CharField(source='color.name', read_only=True)

    class Meta:
        model = Basket
        fields = ['id', 'product_name', 'color', 'color_name', 'quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'color', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'full_name', 'phone_number', 'address', 'created_at', 'status', 'items']
