from django.db import models


class Event(models.Model):
    event_id = models.BigAutoField(primary_key=True)
    device = models.ForeignKey('iot.Device', on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    organisation = models.ForeignKey('users.Organisation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'events'
