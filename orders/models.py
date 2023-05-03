from django.db import models
from djmoney.models.fields import MoneyField
import uuid


class StatusChoices(models.TextChoices):
    received = "PEDIDO REALIZADO"
    on_way = "EM ANDAMENTO"
    delivered = "ENTREGUE"


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="orders"
    )
    status = models.CharField(
        max_length=16, choices=StatusChoices.choices, default=StatusChoices.received
    )
    updated_at = models.DateTimeField(auto_now=True)
    ordered_at = models.DateTimeField(auto_now_add=True)
    price_total = MoneyField(max_digits=19, decimal_places=4, default_currency="BRL")


class ProductsOrders(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
