from django.db import models
import uuid


class Address(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_id = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="address"
    )
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    number = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=10)
