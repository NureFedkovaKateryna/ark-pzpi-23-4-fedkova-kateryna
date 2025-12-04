from rest_framework import viewsets
from .serializers import OrderSerializer, OrderProductSerializer
from .models import Order, OrderProduct


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']


class OrderProductViewSet(viewsets.ModelViewSet):
    serializer_class = OrderProductSerializer
    queryset = OrderProduct.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        order_pk = self.kwargs.get('order')
        if order_pk:
            return OrderProduct.objects.filter(order_id=order_pk)
        return super().get_queryset()

    # def create(self, request, *args, **kwargs):
    #     """
    #     Automatically assigns the author from the URL when creating a book.
    #     """
    #     author_pk = self.kwargs.get('author')  # Get author from URL
    #     request.data['author'] = author_pk  # Assign author before saving
    #     return super().create(request, *args, **kwargs)