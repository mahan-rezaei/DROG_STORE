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
            return Response(ser_data.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'message': 'cart for this user does not exist!'},
                            status=status.HTTP_204_NO_CONTENT)



class CartItemViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request, **kwargs):
        pass

    def retrive(self, request, **kwargs):
        pass

    def create(self, request, **kwargs):
        pass

    def put(self, request, **kwargs):
        pass

    