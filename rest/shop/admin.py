from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_sub', 'parent', 'created_at')
    search_fields = ('name',)
    list_filter  = ('is_sub',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'updated_at')
    search_fields = ('name',)
