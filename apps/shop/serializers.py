from rest_framework import serializers
from .models import Category, ProductImage, ProductColor, Product


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name_uz', 'name_ru', 'subcategories']

    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data


class ColorImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']



class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['id', 'name', 'price', 'images']

class ProductSerializer(serializers.ModelSerializer):
    colors = ProductColorSerializer(many=True, source='productcolor_set')

    class Meta:
        model = Product
        fields = ['id', 'name_uz', 'name_ru', 'description', 'colors']