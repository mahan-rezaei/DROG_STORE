from typing import Any
from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Order, OrderItem, DiscountCode, Address
from shop.models import Product
from .serializer import (
    CartSerlializer, CartItemSerializer, AddressSerializer,
    OrderSerializer, OrderItemSerializer
)
from rest_framework import status


class AddressViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """returns list of user addresses."""
        addresses = Address.objects.filter(user=request.user)
        ser_data = AddressSerializer(addresses, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, **kwargs):
        """returns one of the user addresses."""
        try:
            address = Address.objects.get(pk=kwargs['pk'], user=request.user)
        except Address.DoesNotExist:
            return Response({'message': 'address not found'},
                          status=status.HTTP_404_NOT_FOUND)
        ser_data = AddressSerializer(address)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def create(self, request):
        """create a new address for user."""
        ser_data = AddressSerializer(data=request.data, context={'request': request})
        if ser_data.is_valid(raise_exception=True):
            ser_data.save(user=request.user)
            return Response({
                'message': 'address added successfully',
                'data': ser_data.data
            }, status=status.HTTP_201_CREATED)
        
    def update(self, request, **kwargs):
        """update user address."""
        try:
            address = Address.objects.get(pk=kwargs['pk'], user=request.user)
        except Address.DoesNotExist:
            return Response({'message': 'address not found'},
                          status=status.HTTP_404_NOT_FOUND)
        
        ser_data = AddressSerializer(
            instance=address,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if ser_data.is_valid(raise_exception=True):
            ser_data.save()
            return Response({
                'data': ser_data.data,
                'message': 'address updated successfully.'
            }, status=status.HTTP_200_OK)
        
    def destroy(self, request, **kwargs):
        """remove address."""
        try:
            address = Address.objects.get(pk=kwargs['pk'], user=request.user)
            address.delete()
            return Response({'message': 'Address deleted'}, 
                          status=status.HTTP_204_NO_CONTENT)
        except Address.DoesNotExist:
            return Response({'message': 'Address not found'}, 
                          status=status.HTTP_404_NOT_FOUND)


class CartGetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = request.session.get('cart', {})
        if not cart_items:
            return Response({'message': 'cart is empty!'},
                          status=status.HTTP_204_NO_CONTENT)
        
        # Get product details for cart items
        items_data = []
        total_price = 0
        for product_id, quantity in cart_items.items():
            try:
                product = Product.objects.get(id=product_id)
                items_data.append({
                    'product': product.id,
                    'product_name': product.name,
                    'quantity': quantity,
                    'price': product.price
                })
                total_price += product.price * quantity
            except Product.DoesNotExist:
                continue
        
        return Response({
            'items': items_data,
            'total_price': total_price
        }, status=status.HTTP_200_OK)


class CartItemViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, **kwargs):
        """returns list of cart items."""
        cart_items = request.session.get('cart', {})
        items_data = []
        for product_id, quantity in cart_items.items():
            try:
                product = Product.objects.get(id=product_id)
                items_data.append({
                    'product': product.id,
                    'product_name': product.name,
                    'quantity': quantity,
                    'price': product.price
                })
            except Product.DoesNotExist:
                continue
        return Response(items_data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, **kwargs):
        """returns one of the user cart items."""
        cart_items = request.session.get('cart', {})
        product_id = kwargs['pk']
        
        if product_id not in cart_items:
            return Response({'message': 'item not found'},
                          status=status.HTTP_404_NOT_FOUND)
        
        try:
            product = Product.objects.get(id=product_id)
            return Response({
                'product': product.id,
                'product_name': product.name,
                'quantity': cart_items[product_id],
                'price': product.price
            }, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'message': 'product not found'},
                          status=status.HTTP_404_NOT_FOUND)

    def create(self, request, **kwargs):
        """create one item in user cart."""
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'message': 'product not found'},
                          status=status.HTTP_404_NOT_FOUND)
        
        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + quantity
        request.session['cart'] = cart
        
        return Response({
            'message': 'item added successfully',
            'data': {
                'product': product.id,
                'product_name': product.name,
                'quantity': cart[product_id],
                'price': product.price
            }
        }, status=status.HTTP_201_CREATED)
        
    def update(self, request, **kwargs):
        """update quantity of item in user cart."""
        product_id = kwargs['pk']
        quantity = int(request.data.get('quantity', 1))
        
        cart = request.session.get('cart', {})
        if product_id not in cart:
            return Response({'message': 'item not found'},
                          status=status.HTTP_404_NOT_FOUND)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'message': 'product not found'},
                          status=status.HTTP_404_NOT_FOUND)
        
        cart[product_id] = quantity
        request.session['cart'] = cart
        
        return Response({
            'data': {
                'product': product.id,
                'product_name': product.name,
                'quantity': quantity,
                'price': product.price
            },
            'message': 'item updated successfully.'
        }, status=status.HTTP_200_OK)
        
    def destroy(self, request, **kwargs):
        """remove item from cart."""
        product_id = kwargs['pk']
        cart = request.session.get('cart', {})
        
        if product_id not in cart:
            return Response({'message': 'Item not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        del cart[product_id]
        request.session['cart'] = cart
        return Response({'message': 'Item deleted'}, 
                       status=status.HTTP_204_NO_CONTENT)


class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        cart_items = request.session.get('cart', {})
        if not cart_items:
            return Response({'message': 'Cart is empty'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Validate address
        address_id = request.data.get('address_id')
        if not address_id:
            return Response({'message': 'Address is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            return Response({'message': 'Invalid address'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate total price
        total_price = 0
        order_items = []
        
        for product_id, quantity in cart_items.items():
            try:
                product = Product.objects.get(id=product_id)
                total_price += product.price * quantity
                order_items.append({
                    'product': product,
                    'quantity': quantity,
                    'price': product.price
                })
            except Product.DoesNotExist:
                continue
        
        # Handle discount code if provided
        discount_code = None
        discount_amount = 0
        final_price = total_price
        
        discount_code_str = request.data.get('discount_code')
        if discount_code_str:
            try:
                discount_code = DiscountCode.objects.get(code=discount_code_str)
                if discount_code.is_valid():
                    discount_amount = (total_price * discount_code.discount_percent) // 100
                    final_price = total_price - discount_amount
                else:
                    return Response({
                        'message': 'Discount code is not valid or has expired'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except DiscountCode.DoesNotExist:
                return Response({
                    'message': 'Invalid discount code'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_price=total_price,
            discount_code=discount_code,
            discount_amount=discount_amount,
            final_price=final_price,
            status='pending'
        )
        
        # Create order items
        for item in order_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price']
            )
        
        # Clear cart
        request.session['cart'] = {}
        
        # Return order details
        ser_data = OrderSerializer(order)
        return Response({
            'message': 'Order placed successfully',
            'data': ser_data.data
        }, status=status.HTTP_201_CREATED)



