from django.db import models


class DeviceStatusEnum(models.TextChoices):
    ONLINE = 'online', 'Online'
    OFFLINE = 'offline', 'Offline'
    ERROR = 'error', 'Error'


class Device(models.Model):
    device_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    device_type = models.ForeignKey('iot.DeviceType', null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=DeviceStatusEnum.choices)
    last_connection = models.DateTimeField(auto_now=True)
    organisation = models.ForeignKey('users.Organisation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'devices'