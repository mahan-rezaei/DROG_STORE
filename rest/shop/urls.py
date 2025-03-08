from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('category_list/', views.CategoryListView.as_view()),
    path('retrive_product/<int:pk>/', views.RetriveProductView.as_view()),
    path('product_list/<int:pk>/', views.ProductListView.as_view()),
    path('product_list/', views.ProductListView.as_view()),
]