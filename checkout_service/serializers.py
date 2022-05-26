from .models import Product, Item, Cart
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'images', 'video', 'created_at', 'updated_at']

class ItemSerializer(serializers.ModelSerializer):
    product=ProductSerializer(many=False)
    class Meta:
        model = Item
        fields = ['product', 'amount', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ['username', 'grand_total', 'items']