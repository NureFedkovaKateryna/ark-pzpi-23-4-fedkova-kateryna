from rest_framework import serializers
from apps.menu.models.ingredient_write_off import IngredientWriteOff


class IngredientWriteOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientWriteOff
        fields = '__all__'
