from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializer import CartSerlializer, CartItemSerializer
from rest_framework import status


class CartViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """get user cart"""
        cart = Cart.objects.get(user=request.user)
        ser_data = CartSerlializer(cart)
        return Response(ser_data.data, status=status.HTTP_200_OK)
    
    def 