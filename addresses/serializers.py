from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = [
            "id",
            "user",
            "city",
            "district",
            "street",
            "number",
            "zip_code"
        ]

        read_only_fields = ["id", "user"]

    def create(self, validated_data: dict) -> Address:
        return Address.objects.create(**validated_data)

    def update(self, instance: Address, validated_data: dict) -> Address:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
