from rest_framework import viewsets, status
from rest_framework import mixins
from rest_framework.response import Response
from core.permissions import IsOwner, IsAdmin, IsBarista
from .serializers import OrderSerializer, OrderProductSerializer
from .models import Order, OrderProduct


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAdmin | IsOwner | IsBarista]

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.prefetch_related('order_products')
        if user.role.title == "Admin":
            return orders
        return orders.filter(organisation_id=user.organisation_id)


class OrderProductViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = OrderProductSerializer
    queryset = OrderProduct.objects.all()
    permission_classes = [IsAdmin | IsOwner | IsBarista]

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            order = Order.objects.get(order_id=instance.order_id)
            self.perform_destroy(instance)
            return Response(order, status=status.HTTP_204_NO_CONTENT)
        except OrderProduct.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
