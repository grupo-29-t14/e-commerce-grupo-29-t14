from rest_framework import serializers
from .models import Address
from django.core.exceptions import ValidationError


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

    def validate(self, attrs):

        user_id = self.context['view'].kwargs.get('pk')

        if Address.objects.filter(user_id=user_id).exists():
            raise ValidationError("This user already has a registered address.")
        return attrs

    def create(self, validated_data: dict) -> Address:
        return Address.objects.create(**validated_data)

    def update(self, instance: Address, validated_data: dict) -> Address:
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance
