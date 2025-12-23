from rest_framework import routers
from .views import OrderViewSet, OrderProductViewSet

router = routers.DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')
router.register('order-products', OrderProductViewSet)
urlpatterns = router.urls
