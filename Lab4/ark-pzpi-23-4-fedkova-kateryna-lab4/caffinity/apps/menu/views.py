from rest_framework import mixins, status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.permissions import IsAdmin, IsOwner, IsBarista
from .models.low_ingredient_notification import LowIngredientNotification
from .serializers import IngredientSerializer, ProductSerializer, ProductHintSerializer, ProductIngredientSerializer
from .models import Ingredient, Product, ProductHint, ProductIngredient
from ..orders.serializers import LowIngredientNotificationSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = IsAdmin | IsOwner | IsBarista
        elif self.action  in ('create', 'partial_update', 'destroy'):
            permission_classes = IsAdmin | IsOwner
        else:
            permission_classes = IsAuthenticated
        return [permission_classes()]


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = (
        Product.objects
        .prefetch_related('product_ingredients')
        .prefetch_related('product_hints')
    )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = IsAdmin | IsOwner | IsBarista
        elif self.action  in ('create', 'partial_update', 'destroy'):
            permission_classes = IsAdmin | IsOwner
        else:
            permission_classes = IsAuthenticated
        return [permission_classes()]


class ProductHintViewSet(viewsets.ModelViewSet):
    serializer_class = ProductHintSerializer
    queryset = ProductHint.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']


class ProductHintViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = ProductHintSerializer
    queryset = ProductHint.objects.all()
    permission_classes = [IsAdmin | IsOwner]

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            order = ProductHint.objects.get(order_id=instance.order_id)
            self.perform_destroy(instance)
            return Response(order, status=status.HTTP_204_NO_CONTENT)
        except ProductHint.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ProductIngredientViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = ProductIngredientSerializer
    queryset = ProductIngredient.objects.all()
    permission_classes = [IsAdmin | IsOwner]

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            product = Product.objects.get(product_id=instance.product_id)
            self.perform_destroy(instance)
            return Response(product, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LowIngredientNotificationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = LowIngredientNotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return LowIngredientNotification.objects.filter(organisation_id=user.organisation_id).order_by("-created_at")
