from django.db.models import Count
from rest_framework import mixins
from rest_framework import viewsets
from apps.analytics.serializers import IngredientWriteOffSerializer
from apps.menu.models.ingredient_write_off import IngredientWriteOff
from apps.orders.serializers import BaristaPerformanceSerializer
from apps.users.models import User


class BaristaPerformanceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = BaristaPerformanceSerializer

    def get_queryset(self):
        user = self.request.user
        organisation_id = user.organisation_id
        data = (
            User.objects
            .filter(organisation_id=organisation_id)
            .annotate(count=Count("orders"))
            .values("username", "email", "count")
            .order_by("-count")
        )
        return data


class IngredientWriteOffViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IngredientWriteOffSerializer

    def get_queryset(self):
        user = self.request.user
        return IngredientWriteOff.objects.filter(organisation_id=user.organisation_id)

