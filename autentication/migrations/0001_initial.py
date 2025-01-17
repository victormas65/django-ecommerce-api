# Generated by Django 5.1.2 on 2024-10-16 01:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RoleModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "name",
                    models.CharField(
                        choices=[("ADMIN", "Administrador"), ("SELLER", "Vendedor")],
                        default="SELLER",
                        max_length=10,
                    ),
                ),
                ("status", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Rol",
                "verbose_name_plural": "Roles",
                "db_table": "roles",
            },
        ),
        migrations.CreateModel(
            name="UserModel",
            fields=[
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password", models.CharField(max_length=120)),
                ("status", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_superuser", models.BooleanField(default=False)),
                (
                    "rol",
                    models.ForeignKey(
                        db_column="role_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="users",
                        to="autentication.rolemodel",
                    ),
                ),
            ],
            options={
                "verbose_name": "Usuario",
                "verbose_name_plural": "Usuarios",
                "db_table": "users",
            },
        ),
    ]
