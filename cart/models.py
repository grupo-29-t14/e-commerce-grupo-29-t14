from django.db import models
import uuid


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
    quantity = models.IntegerField(default=1)
