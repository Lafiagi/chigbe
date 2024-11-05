# Generated by Django 5.1.2 on 2024-10-26 19:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("authy", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Drug",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(max_length=255)),
                ("dosage", models.CharField(max_length=50)),
                ("batch_number", models.CharField(max_length=50)),
                ("manufacture_date", models.DateField()),
                ("expiry_date", models.DateField()),
                ("manufacturer", models.CharField(max_length=255)),
                ("unique_code", models.CharField(max_length=50, unique=True)),
                (
                    "business",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="authy.business"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
