from django.db.models import F
from rest_framework import serializers
from core.utils import save_with_organisation
from .models import Order, OrderProduct
from .models.order import StatusEnum
from ..menu.models import Product, Ingredient
from ..menu.models.low_ingredient_notification import LowIngredientNotification
from ..users.models import User


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['order_product_id', 'quantity', 'product']


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True)
    organisation = serializers.PrimaryKeyRelatedField(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        if request:
            if request.method == 'POST':
                fields.pop('order_products', None)
            elif request.method in ('PATCH', 'PUT'):
                fields['order_products'].read_only = False
            else:
                fields['order_products'].read_only = True
        return fields

    def get_total_price(self, obj):
        total = 0
        for op in obj.order_products.all():
            total += op.product.price * op.quantity
        return total

    def create(self, validated_data):
        request = self.context.get('request')
        order = save_with_organisation(request, validated_data, Order)
        return order

    def update(self, instance, validated_data):
        order_products = validated_data.pop('order_products', None)
        instance = super().update(instance, validated_data)
        if order_products:
            for op_data in order_products:
                product_obj = op_data.get('product')
                quantity = op_data.get('quantity')

                if isinstance(product_obj, Product):
                    product_id = product_obj.product_id
                else:
                    product_id = product_obj

                OrderProduct.objects.update_or_create(
                    order_id=instance.order_id,
                    product_id=product_id,
                    defaults={
                        'quantity': quantity,
                        'organisation_id': instance.organisation_id
                    }
                )

        if instance.status == StatusEnum.DONE:
            for op in instance.order_products.all():
                product = op.product
                total_product_quantity = op.quantity  
                for pi in product.product_ingredients.all():
                    Ingredient.objects.filter(ingredient_id=pi.ingredient.ingredient_id).update(
                        quantity=F('quantity') - pi.quantity * total_product_quantity
                    )

                    ingredient = Ingredient.objects.get(ingredient_id=pi.ingredient.ingredient_id)
                    current_quantity = ingredient.quantity
                    LowIngredientNotification.objects.create(
                        product_id=product.product_id,
                        organisation_id=product.organisation_id,
                        current_quantity=current_quantity
                    )
        return instance


class LowIngredientNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LowIngredientNotification
        fields = '__all__'


class BaristaPerformanceSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "count"]
