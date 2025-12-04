from django.db import models


class Ingredient(models.Model):
    ingredient_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=9, decimal_places=3)
    unit = models.CharField(max_length=50)
    min_amount = models.DecimalField(max_digits=9, decimal_places=3, default=0)
    organisation = models.ForeignKey('users.Organisation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'ingredients'
