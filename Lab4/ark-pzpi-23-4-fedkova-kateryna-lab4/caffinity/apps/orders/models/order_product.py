from django.db import models


class OrderProduct(models.Model):
    order_product_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey('menu.Product', on_delete=models.PROTECT)
    quantity = models.IntegerField()
    organisation = models.ForeignKey('users.Organisation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders_products'