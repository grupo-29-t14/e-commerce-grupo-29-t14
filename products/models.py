from django.db import models
import uuid
from djmoney.models.fields import MoneyField
from django.core.validators import MinValueValidator


class CategoryChoices(models.TextChoices):
    T_SHIRTS = "Camisetas"
    SHIRTS = "Camisas"
    BLOUSES = "Blusas"
    DRESSES = "Vestidos"
    SKIRTS = "Saias"
    PANTS = "Calças"
    SHORTS = "Shorts"
    JACKETS = "Jaquetas"
    COATS = "Casacos"
    BATHING_SUITS = "Roupas de banho"
    SPORTS = "Roupas esportivas"
    UNDERWEAR = "Roupas íntimas"
    SLEEPING_CLOTHES = "Roupas para dormir"
    MATERNITY_CLOTHES = "Roupas de maternidade"
    BIG_SIZE_CLOTHES = "Roupas de tamanho grande"
    PARTY_EVENTS_CLOTHES = "Roupas para festas e eventos"
    WORK_CLOTHES = "Roupas para trabalho"
    SCHOOL_UNIFORM = "Uniformes escolares"
    WINTER_CLOTHES = "Roupas de inverno"
    SUMMER_CLOTHES = "Roupas de verão"


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    seller = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=50, choices=CategoryChoices.choices)
    stock = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    price = MoneyField(max_digits=19, decimal_places=4, default_currency="BRL")
    available = models.BooleanField(default=True)
