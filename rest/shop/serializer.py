from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'sub_categories')

    def get_sub_categories(self, obj):
        subs = obj.sub_categories.all()
        ser_data = CategorySerializer(instance=subs, many=True).data
        return ser_data
