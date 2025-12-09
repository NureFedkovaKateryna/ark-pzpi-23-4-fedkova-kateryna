from django.db import models


class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    organisation = models.ForeignKey('users.Organisation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'

