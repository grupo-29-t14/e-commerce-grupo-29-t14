from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=120, unique=True)
    is_seller = models.BooleanField(default=False)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=120)
