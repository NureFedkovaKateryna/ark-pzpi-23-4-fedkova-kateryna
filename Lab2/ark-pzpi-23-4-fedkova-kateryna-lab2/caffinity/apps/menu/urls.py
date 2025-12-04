from rest_framework import routers
from .views import IngredientViewSet, ProductViewSet, ProductHintViewSet, ProductIngredientViewSet

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('products', ProductViewSet)
router.register('product-hints', ProductHintViewSet)
router.register('product-ingredients', ProductIngredientViewSet)
urlpatterns = router.urls
