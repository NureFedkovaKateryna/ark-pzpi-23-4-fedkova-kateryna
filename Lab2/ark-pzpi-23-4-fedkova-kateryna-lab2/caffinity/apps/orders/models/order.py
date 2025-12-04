from django.db import models


class StatusEnum(models.TextChoices):
    IN_PROGRESS = 'in progress', 'In progress'
    DONE = 'done', 'Done'
    CANCELLED = 'cancelled', 'Cancelled'



class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('users.User', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=StatusEnum.choices)
    organisation = models.ForeignKey('users.Organisation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'