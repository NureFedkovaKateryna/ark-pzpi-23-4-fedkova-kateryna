from rest_framework import serializers
from .models import Ingredient, Product, ProductHint, ProductIngredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductHintSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductHint
        fields = '__all__'


class ProductIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductIngredient
        fields = '__all__'
