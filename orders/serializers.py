from rest_framework import serializers
from .models import StatusChoices
from djmoney.contrib.django_rest_framework import MoneyField


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.ChoiceField(choices=StatusChoices.choices, default=StatusChoices.received, max_length=16)
    updated_at = serializers.DateTimeField()
    ordered_at = serializers.DateTimeField()
    price_total = MoneyField(max_digits=19, decimal_places=4)
