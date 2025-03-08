from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('category_list/', views.CategoryListView.as_view()),
]