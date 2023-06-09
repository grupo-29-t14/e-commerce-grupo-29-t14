from typing import Any
from django.db import models
from django.core.validators import MinValueValidator
from djmoney.models.fields import MoneyField
import uuid
from products.models import Product


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    buyer = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="cart"
    )


class CartProducts(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
    )
    cart = models.ForeignKey(
        "cart.Cart", on_delete=models.CASCADE, related_name="products"
    )
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    price = MoneyField(
        default=1, max_digits=19, decimal_places=4, default_currency="BRL"
    )
