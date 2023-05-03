# Generated by Django 4.2.1 on 2023-05-03 17:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("city", models.CharField(max_length=50)),
                ("district", models.CharField(max_length=50)),
                ("street", models.CharField(max_length=50)),
                ("number", models.CharField(max_length=10)),
                ("zip_code", models.CharField(max_length=10)),
            ],
        ),
    ]