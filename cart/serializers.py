from rest_framework import serializers, validators
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

        depth = 1


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartProducts
