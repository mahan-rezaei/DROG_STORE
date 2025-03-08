from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'subcategories')

    def get_subcategories(self, obj):
        subs = obj.sub_categories.all()
        ser_data = CategorySerializer(instance=subs, many=True).data
        return ser_data
