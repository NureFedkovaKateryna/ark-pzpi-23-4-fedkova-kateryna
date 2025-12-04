from rest_framework import routers
from .views import OrderViewSet, OrderProductViewSet

router = routers.DefaultRouter()
router.register('orders', OrderViewSet)
router.register('order-products', OrderProductViewSet)
urlpatterns = router.urls
