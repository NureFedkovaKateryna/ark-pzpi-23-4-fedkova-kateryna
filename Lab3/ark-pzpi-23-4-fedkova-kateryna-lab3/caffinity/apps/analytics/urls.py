from rest_framework import routers
from apps.analytics.views import BaristaPerformanceViewSet, IngredientWriteOffViewSet

router = routers.DefaultRouter()
router.register('barista-performance', BaristaPerformanceViewSet, basename='barista-performance')
router.register('ingredient-write-off-history', IngredientWriteOffViewSet, basename='ingredient-write-off-history')

urlpatterns = router.urls
