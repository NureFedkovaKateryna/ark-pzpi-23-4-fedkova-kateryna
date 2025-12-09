from django.db import models


class SensorType(models.Model):
    sensor_type_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    organisation = models.ForeignKey('users.Organisation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sensor_types'