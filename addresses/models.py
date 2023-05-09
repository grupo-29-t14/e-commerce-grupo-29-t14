from django.db import models
import uuid
from django.core.validators import MinValueValidator


class Address(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="address"
    )
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    number = models.IntegerField(validators=[MinValueValidator(0)])
    zip_code = models.IntegerField(validators=[MinValueValidator(0)])
