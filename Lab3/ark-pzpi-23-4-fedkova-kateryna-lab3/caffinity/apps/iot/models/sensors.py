from django.db import models


class Sensor(models.Model):
    sensor_id = models.BigAutoField(primary_key=True)
    device = models.ForeignKey('iot.Device', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    sensor_type = models.ForeignKey('iot.SensorType', null=True, on_delete=models.SET_NULL)
    unit = models.CharField(max_length=50)
    min_value = models.IntegerField()
    max_value = models.IntegerField()
    organisation = models.ForeignKey('users.Organisation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sensors'
