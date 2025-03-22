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
    
    def list(self, request, **kwargs):
        """returns list of cart items"""
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'message': 'cart for this user is not regonized'},
                            status=status.HTTP_400_BAD_REQUEST)
        items = CartItem.objects.filter(cart=cart)
        ser_data = CartItemSerializer(items, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        """create one item in user cart"""
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'message': 'cart for this user is not regonized'},
                            status=status.HTTP_400_BAD_REQUEST)
        ser_data = CartItemSerializer(data=request.data)
        if ser_data.is_valid(raise_exception=True):
            ser_data.save(cart=cart)
            return Response({'message': 'item added successfully', 'data': ser_data.data},
                            status=status.HTTP_201_CREATED)
        

    def put(self, request, **kwargs):
        pass

    