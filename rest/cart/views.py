from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializer import CartSerlializer, CartItemSerializer
from rest_framework import status


class CartGetView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            ser_data = CartSerlializer(cart)
            return Response(ser_data.data)
        except Cart.DoesNotExist:
            return Response({'message': 'cart for this user does not exist!'})



class CartItemViewSet(ViewSet):
    pass
    