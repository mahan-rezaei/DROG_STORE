from typing import Any
from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from shop.models import Product
from .serializer import CartSerlializer, CartItemSerializer
from rest_framework import status


class CartGetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            ser_data = CartSerlializer(cart)
            return Response(ser_data.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'message': 'cart for this user does not exist!'},
                            status=status.HTTP_204_NO_CONTENT)



class CartItemViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.cart, created = Cart.objects.get_or_create(user=request.user)
        
    
    def list(self, request, **kwargs):
        """returns list of cart items"""
        items = CartItem.objects.filter(cart=self.cart)
        ser_data = CartItemSerializer(items, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)
    
    def retrive(self, request, **kwargs):
        try:
            item = CartItem.objects.get(pk=kwargs['pk'], cart__user=request.user)
        except:
            return Response({'message': 'this item is None'},
                            status=status.HTTP_204_NO_CONTENT)
        ser_data = CartItemSerializer(item)
        return Response(ser_data.data)

    def create(self, request, **kwargs):
        """create one item in user cart"""
        ser_data = CartItemSerializer(data=request.data)
        if ser_data.is_valid(raise_exception=True):
            ser_data.save(cart=self.cart)
            return Response({'message': 'item added successfully', 'data': ser_data.data},
                            status=status.HTTP_201_CREATED)
        
    def update(self, request, **kwargs):
        """update quantitiy of item in user cart"""
        item = CartItem.objects.filter(pk=kwargs['pk'], cart__user=request.user)
        ser_data = CartItemSerializer(item, data=request.data, partial=True)
        if ser_data.is_valid(raise_exception=True):
            ser_data.save()
            return Response({'data': ser_data.data, 'message': 'item updated successfully.'},
                            status=status.HTTP_200_OK)
        


    