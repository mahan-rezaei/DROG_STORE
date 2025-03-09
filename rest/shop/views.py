from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializer import CategorySerializer, ProductSerializer
from .models import Category, Product


class CategoryListView(ListAPIView):
    """return list of categories with theyr sub categories"""

    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_sub=False)


class RetriveProductView(RetrieveAPIView):
    """return on product (id most sent in url)"""

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductListView(ListAPIView):
    """return list of products"""

    serializer_class = ProductSerializer

    def get_queryset(self):
        if self.kwargs.get('pk'):
            return Product.objects.filter(category=self.kwargs['pk'])
        return Product.objects.all()