from rest_framework import serializers
from .models import Cart, CartItem
from .custom_fields import CustomUserPhoneField


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'quantity')


class CartSerlializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    user = CustomUserPhoneField(read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'created_at')    