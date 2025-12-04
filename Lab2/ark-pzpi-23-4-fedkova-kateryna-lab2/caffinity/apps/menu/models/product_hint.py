from django.db import models


class ProductHint(models.Model):
    product_hint_id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey('menu.Product', on_delete=models.CASCADE)
    step_number = models.IntegerField()
    description = models.TextField()
    organisation = models.ForeignKey('users.Organisation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_hints'