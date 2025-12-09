from django.db import models


class LowIngredientNotification(models.Model):
    low_ingredient_notification = models.BigAutoField(primary_key=True)
    product = models.ForeignKey('menu.Product', on_delete=models.CASCADE)
    organisation = models.ForeignKey('users.Organisation', on_delete=models.CASCADE)
    current_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
