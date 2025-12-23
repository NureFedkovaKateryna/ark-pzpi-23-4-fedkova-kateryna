from rest_framework import serializers
from core.utils import save_with_organisation
from .models import Ingredient, Product, ProductHint, ProductIngredient


class IngredientSerializer(serializers.ModelSerializer):
    organisation = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Ingredient
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        ingredient = save_with_organisation(request, validated_data, Ingredient)
        return ingredient


class ProductIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductIngredient
        fields = ['product_ingredient_id', 'ingredient', 'quantity']


class ProductHintSerializer(serializers.ModelSerializer):
    product = serializers.CharField(read_only=True)
    organisation = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = ProductHint
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    product_ingredients = ProductIngredientSerializer(many=True, required=False)
    product_hints = ProductHintSerializer(many=True)
    organisation = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        return fields

    def create(self, validated_data):
        product_ingredients = validated_data.pop('product_ingredients', [])
        product_hints = validated_data.pop('product_hints', [])
        request = self.context.get('request')
        product = save_with_organisation(request, validated_data, Product)
        if product_ingredients:
            for ingredient in product_ingredients:
                ProductIngredient.objects.create(
                    product_id=product.product_id,
                    ingredient=ingredient.get('ingredient'),
                    quantity=ingredient.get('quantity'),
                    organisation_id=product.organisation.organisation_id
                )
        if product_hints:
            for hint in product_hints:
                ProductHint.objects.create(
                    product_id=product.product_id,
                    step_number=hint.get('step_number'),
                    description=hint.get('description'),
                    organisation_id=product.organisation_id
                )
        return product

    def update(self, instance, validated_data):
        product_hints = validated_data.pop('product_hints', [])
        instance = super().update(instance, validated_data)
        if product_hints:
            for hint in product_hints:
                ProductHint.objects.update_or_create(
                    product_id=instance.product_id,
                    step_number=hint.get('step_number'),
                    defaults={
                    'description': hint.get('description'),
                    'organisation_id': instance.organisation_id
                })
        return instance

