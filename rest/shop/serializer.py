from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'subcategories')

    def get_subcategories(self, obj):
        subs = obj.sub_categories.all()
        ser_data = SubCategorySerializer(instance=subs, many=True).data
        return ser_data


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')



class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ('id', 'name', 'image', 'price', 'stock', 'category')

    def get_category(self, obj):
        cat = obj.category.filter(is_sub=False)
        ser_data = ProductCategorySerializer(instance=cat, many=True).data
        return ser_data
