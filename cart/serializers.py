from rest_framework import serializers, validators
from djmoney.contrib.django_rest_framework import MoneyField
from . import models


class CartSerializer(serializers.ModelSerializer):
    buyer_id = serializers.CharField(
        validators=[
            validators.UniqueValidator(
                queryset=models.Cart.objects.all(), message="User already has cart"
            )
        ]
    )

    class Meta:
        model = models.Cart
        fields = ["id", "buyer_id", "products"]

        extra_kwargs = {
            "buyer_id": {"read_only": True},
        }

        depth = 2


class CartProductSerializer(serializers.ModelSerializer):
    price = MoneyField(
        default=1, max_digits=19, decimal_places=4, default_currency="BRL"
    )

    def update(self, instance: models.CartProducts, validated_data: dict):
        if self.initial_data.get("operation") == "sum":
            instance.price += instance.price / instance.quantity
            instance.quantity += 1
            instance.save()

        elif instance.quantity - 1 == 0:
            instance.delete()

        else:
            instance.price -= instance.price / instance.quantity
            instance.quantity -= 1
            instance.save()

        return instance

    class Meta:
        model = models.CartProducts
        fields = ["id", "product", "cart", "quantity", "price"]

        extra_kwargs = {
            "cart": {"read_only": True},
            "product": {"read_only": True},
            "operation": {"read_only": True},
        }
