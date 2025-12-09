from django.db import models


class ProductIngredient(models.Model):
    product_ingredient_id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey('menu.Product', on_delete=models.CASCADE, related_name='product_ingredients')
    ingredient = models.ForeignKey('menu.Ingredient', on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=9, decimal_places=3)
    organisation = models.ForeignKey('users.Organisation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_ingredients'
