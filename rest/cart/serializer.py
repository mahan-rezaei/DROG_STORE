from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer():
    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'quantity')


class CartSerlializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'created_at')    
        read_only_fields = ('user',)