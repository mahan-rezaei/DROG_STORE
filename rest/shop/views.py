from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializer import CategorySerializer
from .models import Category


class CategoryView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
