from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializer import CategorySerializer, ProductSerializer
from .models import Category, Product


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_sub=False)


class RetriveProductView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        if self.kwargs.get('pk'):
            return Product.objects.filter(category=self.kwargs['pk'])
        return Product.objects.all()