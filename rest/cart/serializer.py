from rest_framework import serializers
from .models import Cart, CartItem, Address, Order, OrderItem
from .custom_fields import CustomUserPhoneField


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'title', 'receiver_name', 'receiver_phone', 
                 'province', 'city', 'postal_code', 'address', 'is_default')
        read_only_fields = ('id', 'created_at')

    def validate(self, data):
        # اگر این آدرس به عنوان پیش‌فرض انتخاب شده، سایر آدرس‌های پیش‌فرض را غیرفعال می‌کنیم
        if data.get('is_default'):
            user = self.context['request'].user
            Address.objects.filter(user=user, is_default=True).update(is_default=False)
        return data


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


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'quantity', 'price')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    user = CustomUserPhoneField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'address', 'total_price', 'discount_amount', 
                 'final_price', 'status', 'items', 'created_at')    