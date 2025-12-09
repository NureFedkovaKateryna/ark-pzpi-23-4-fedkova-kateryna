from rest_framework import routers
from .views import IngredientViewSet, ProductViewSet, ProductHintViewSet, ProductIngredientViewSet, \
    LowIngredientNotificationViewSet

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('products', ProductViewSet)
router.register('product-hints', ProductHintViewSet)
router.register('product-ingredients', ProductIngredientViewSet)
router.register("notifications/low-ingredient", LowIngredientNotificationViewSet, basename='low-ingredients')
urlpatterns = router.urls
