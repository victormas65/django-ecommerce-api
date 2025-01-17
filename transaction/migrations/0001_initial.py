# Generated by Django 5.1.2 on 2024-10-16 01:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("warehouse", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomerModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=200)),
                ("document_number", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
            ],
            options={
                "verbose_name": "Cliente",
                "verbose_name_plural": "Clientes",
                "db_table": "customers",
            },
        ),
        migrations.CreateModel(
            name="SaleModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("code", models.CharField(max_length=100)),
                ("total", models.FloatField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pendiente"),
                            ("COMPLETED", "Completado"),
                            ("CANCELLED", "Cancelado"),
                            ("DELETED", "Eliminado"),
                        ],
                        default="PENDING",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "customer",
                    models.ForeignKey(
                        db_column="customer_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sales",
                        to="transaction.customermodel",
                    ),
                ),
            ],
            options={
                "verbose_name": "Venta",
                "verbose_name_plural": "Ventas",
                "db_table": "sales",
            },
        ),
        migrations.CreateModel(
            name="SaleDetailModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("quantity", models.IntegerField()),
                ("price", models.FloatField()),
                ("subtotal", models.FloatField()),
                (
                    "product",
                    models.ForeignKey(
                        db_column="product_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_details",
                        to="warehouse.productmodel",
                    ),
                ),
                (
                    "sale",
                    models.ForeignKey(
                        db_column="sale_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sale_details",
                        to="transaction.salemodel",
                    ),
                ),
            ],
            options={
                "verbose_name": "Detalle de venta",
                "verbose_name_plural": "Detalles de venta",
                "db_table": "sale_details",
            },
        ),
    ]
