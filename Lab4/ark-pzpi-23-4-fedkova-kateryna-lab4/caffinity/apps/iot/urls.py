from rest_framework import routers
from .views import CommandViewSet, CommandTypeViewSet, DeviceViewSet, DeviceLogViewSet, DeviceTypeViewSet, EventViewSet, SensorTypeViewSet, SensorViewSet

router = routers.DefaultRouter()
router.register('commands', CommandViewSet)
router.register('command-types', CommandTypeViewSet)
router.register('devices', DeviceViewSet)
router.register('device-logs', DeviceLogViewSet)
router.register('device-types', DeviceTypeViewSet)
router.register('events', EventViewSet)
router.register('sensor-types', SensorTypeViewSet)
router.register('sensors', SensorViewSet)
urlpatterns = router.urls
