from django.db import models


class StatusEnum(models.TextChoices):
    IN_PROGRESS = 'in progress'
    DONE = 'done'
    CANCELLED = 'cancelled'


class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('users.User', null=True, on_delete=models.SET_NULL, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=StatusEnum.choices)
    organisation = models.ForeignKey('users.Organisation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'