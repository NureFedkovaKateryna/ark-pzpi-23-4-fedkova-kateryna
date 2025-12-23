from django.db import models


class DeviceLog(models.Model):
    device_log_id = models.BigAutoField(primary_key=True)
    sensor = models.ForeignKey('iot.Sensor', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(null=True, blank=True)
    organisation = models.ForeignKey('users.Organisation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'device_logs'

