from rest_framework import viewsets
from .serializers import CommandSerializer, CommandTypeSerializer, DeviceSerializer, DeviceLogSerializer, \
    DeviceTypeSerializer, EventSerializer, SensorTypeSerializer, SensorSerializer
from .models import Command, CommandType, Device, DeviceLog, DeviceType, Event, SensorType, Sensor


class CommandViewSet(viewsets.ModelViewSet):
    serializer_class = CommandSerializer
    queryset = Command.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']


class CommandTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CommandTypeSerializer
    queryset = CommandType.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']


class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']


class DeviceLogViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceLogSerializer
    queryset = DeviceLog.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']


class DeviceTypeViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceTypeSerializer
    queryset = DeviceType.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']


class SensorTypeViewSet(viewsets.ModelViewSet):
    serializer_class = SensorTypeSerializer
    queryset = SensorType.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']


class SensorViewSet(viewsets.ModelViewSet):
    serializer_class = SensorSerializer
    queryset = Sensor.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
