# Поганий приклад

from rest_framework.views import APIView
from rest_framework.response import Response
from myapp.models import Order


class OrderStatsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        orders = Order.objects.filter(user=user)
        total_price = 0
        total_items = 0
        for order in orders:
            for item in order.items.all():
                total_price += item.price * item.quantity
                total_items += item.quantity

        return Response({
            "username": user.username,
            "total_orders": orders.count(),
            "total_items": total_items,
            "total_price": total_price,
        })


# Гарний приклад

class OrderStatsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        orders = Order.objects.filter(user=user)
        stats = self._calculate_order_stats(orders)

        return Response({
            "username": user.username,
            "total_orders": orders.count(),
            **stats,
        })

    def _calculate_order_stats(self, orders):
        total_price = 0
        total_items = 0
        for order in orders:
            for item in order.items.all():
                total_price += item.price * item.quantity
                total_items += item.quantity

        return {
            "total_items": total_items,
            "total_price": total_price,
        }


# Поганий приклад

class OrderStatsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user)
        total_price = 0
        for order in orders:
            if order.type == "standard":
                total_price += order.price
            elif order.type == "express":
                total_price += order.price + 50
            elif order.type == "bulk":
                total_price += order.price * 0.9  

        return Response({
            "total_orders": orders.count(),
            "total_price": total_price,
        })


# Гарний приклад

from abc import ABC, abstractmethod

class OrderBase(ABC):
    def __init__(self, price):
        self.price = price

    @abstractmethod
    def calculate_price(self):
        pass


class StandardOrder(OrderBase):
    def calculate_price(self):
        return self.price


class ExpressOrder(OrderBase):
    def calculate_price(self):
        return self.price + 50


class BulkOrder(OrderBase):
    def calculate_price(self):
        return self.price * 0.9


ORDER_TYPE_MAPPING = {
    "standard": StandardOrder,
    "express": ExpressOrder,
    "bulk": BulkOrder,
}


class OrderStatsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user)
        total_price = 0
        for order in orders:
            order_class = ORDER_TYPE_MAPPING.get(order.type, StandardOrder)
            order_obj = order_class(order.price)
            total_price += order_obj.calculate_price()

        return Response({
            "total_orders": orders.count(),
            "total_price": total_price,
        })


# Поганий приклад

from datetime import timedelta
from django.utils import timezone


class OrderCancelAPIView(APIView):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['order_id'])
        now = timezone.now()
        can_cancel = False
        if order.status != 'delivered':
            if not order.cancelled:
                if order.created_at > now - timedelta(days=1):
                    can_cancel = True

        return Response({
            "order_id": order.id,
            "can_cancel": can_cancel,
        })


# Гарний приклад


class OrderCancelAPIView(APIView):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['order_id'])
        now = timezone.now()
        can_cancel = (
            order.status != 'delivered' and
            not order.cancelled and
            order.created_at > now - timedelta(days=1)
        )

        return Response({
            "order_id": order.id,
            "can_cancel": can_cancel,
        })

