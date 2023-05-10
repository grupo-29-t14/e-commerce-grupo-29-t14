from rest_framework import serializers
from .models import Order, ProductsOrders


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        depth = 1
        read_only_fields = ["id"]

    def create(self, validated_data):
        return Order.objects.create(**validated_data)


class ProductsOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsOrders
        fields = "__all__"
        depth = 1
        read_only_fields = ["id", "product", "order"]

    def create(self, validated_data):
        return ProductsOrders.objects.create(**validated_data)


class ListOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["id"]


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["id", "user", "seller", "updated_at", "ordered_at", "price_total"]

    def update(self, instance: Order, validated_data: dict) -> Order:
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance
