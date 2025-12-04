from rest_framework import viewsets
from .serializers import IngredientSerializer, ProductSerializer, ProductHintSerializer, ProductIngredientSerializer
from .models import Ingredient, Product, ProductHint, ProductIngredient


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']


class ProductHintViewSet(viewsets.ModelViewSet):
    serializer_class = ProductHintSerializer
    queryset = ProductHint.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']


class ProductIngredientViewSet(viewsets.ModelViewSet):
    serializer_class = ProductIngredientSerializer
    queryset = ProductIngredient.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
