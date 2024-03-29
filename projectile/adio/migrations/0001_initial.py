# Generated by Django 4.1.7 on 2023-08-03 11:27

import adio.utils
import autoslug.fields
import dirtyfields.dirtyfields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AdOrganization",
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
                (
                    "uid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False,
                        populate_from=adio.utils.get_ad_organization_slug,
                        unique=True,
                    ),
                ),
                ("start_date", models.DateField()),
                (
                    "ad_days",
                    models.CharField(
                        choices=[("60_DAYS", "60 Days"), ("30_DAYS", "30 Days")],
                        db_index=True,
                        max_length=20,
                    ),
                ),
                ("stop_date", models.DateField()),
                (
                    "total_price",
                    models.DecimalField(decimal_places=3, default=0, max_digits=19),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("ACTIVE", "Active"),
                            ("REMOVED", "Removed"),
                        ],
                        db_index=True,
                        default="PENDING",
                        max_length=20,
                    ),
                ),
                ("view_count", models.PositiveBigIntegerField(default=0)),
                ("click_count", models.PositiveBigIntegerField(default=0)),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="AdProduct",
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
                (
                    "uid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False,
                        populate_from=adio.utils.get_ad_product_slug,
                        unique=True,
                    ),
                ),
                ("start_date", models.DateField()),
                (
                    "ad_days",
                    models.CharField(
                        choices=[("60_DAYS", "60 Days"), ("30_DAYS", "30 Days")],
                        db_index=True,
                        max_length=20,
                    ),
                ),
                ("stop_date", models.DateField()),
                (
                    "total_price",
                    models.DecimalField(decimal_places=3, default=0, max_digits=19),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("ACTIVE", "Active"),
                            ("REMOVED", "Removed"),
                        ],
                        db_index=True,
                        default="PENDING",
                        max_length=20,
                    ),
                ),
                ("view_count", models.PositiveBigIntegerField(default=0)),
                ("click_count", models.PositiveBigIntegerField(default=0)),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="AdProject",
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
                (
                    "uid",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        editable=False,
                        populate_from=adio.utils.get_ad_project_slug,
                        unique=True,
                    ),
                ),
                ("start_date", models.DateField()),
                (
                    "ad_days",
                    models.CharField(
                        choices=[("60_DAYS", "60 Days"), ("30_DAYS", "30 Days")],
                        db_index=True,
                        max_length=20,
                    ),
                ),
                ("stop_date", models.DateField()),
                (
                    "total_price",
                    models.DecimalField(decimal_places=3, default=0, max_digits=19),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("ACTIVE", "Active"),
                            ("REMOVED", "Removed"),
                        ],
                        db_index=True,
                        default="PENDING",
                        max_length=20,
                    ),
                ),
                ("view_count", models.PositiveBigIntegerField(default=0)),
                ("click_count", models.PositiveBigIntegerField(default=0)),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
    ]
