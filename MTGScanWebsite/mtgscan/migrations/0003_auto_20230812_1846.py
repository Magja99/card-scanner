# Generated by Django 3.2.20 on 2023-08-12 16:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("mtgscan", "0002_auto_20230812_1842"),
    ]

    operations = [
        migrations.CreateModel(
            name="Possesion",
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
                ("cardId", models.ManyToManyField(to="mtgscan.Card")),
                ("userId", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
