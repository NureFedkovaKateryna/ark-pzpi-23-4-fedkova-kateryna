from django.db import models

class StatusEnum(models.TextChoices):
    IN_PROGRESS = 'in progress', 'In progress'
    DONE = 'done', 'Done'
    CANCELLED = 'cancelled', 'Cancelled'

class Command(models.Model):
    command_id = models.BigAutoField(primary_key=True)
    device = models.ForeignKey('iot.Device', on_delete=models.CASCADE)
    command_type = models.ForeignKey('iot.CommandType', null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=StatusEnum.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    executed_at = models.DateTimeField(null=True)
    product = models.ForeignKey('menu.Product', null=True, on_delete=models.SET_NULL)
    organisation = models.ForeignKey('users.Organisation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'commands'
