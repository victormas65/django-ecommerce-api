# Generated by Django 5.1.2 on 2024-10-17 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("autentication", "0002_alter_rolemodel_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rolemodel",
            name="name",
            field=models.CharField(
                choices=[
                    ("ADMIN", "Administrador"),
                    ("SELLER", "Vendedor"),
                    ("CUSTOMER", "Cliente"),
                ],
                default="SELLER",
                max_length=10,
                unique=True,
            ),
        ),
    ]
