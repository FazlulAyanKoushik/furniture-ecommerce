# Generated by Django 4.1.7 on 2023-06-19 17:25

import autoslug.fields
import dirtyfields.dirtyfields
from django.db import migrations, models
import django.db.models.deletion
import populario.utils
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accountio", "0005_alter_historicalorganization_kind_and_more"),
        ("collabio", "0003_alter_historicalprojectparticipant_status_and_more"),
        ("catalogio", "0011_material_productmaterialconnector"),
    ]

    operations = [
        migrations.CreateModel(
            name="PopularProject",
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
                        populate_from=populario.utils.get_popular_project_slug,
                        unique=True,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DRAFT", "Draft"),
                            ("ACTIVE", "Active"),
                            ("ARCHIVED", "Archived"),
                            ("HIDDEN", "Hidden"),
                            ("REMOVED", "Removed"),
                        ],
                        default="ACTIVE",
                        max_length=20,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accountio.organization",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="collabio.project",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="PopularProduct",
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
                        populate_from=populario.utils.get_popular_product_slug,
                        unique=True,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DRAFT", "Draft"),
                            ("PUBLISHED", "Published"),
                            ("UNPUBLISHED", "Unpublished"),
                            ("ARCHIVED", "Archived"),
                            ("HIDDEN", "Hidden"),
                            ("REMOVED", "Removed"),
                        ],
                        default="PUBLISHED",
                        max_length=20,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accountio.organization",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalogio.product",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name="PopularOrganization",
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
                        populate_from=populario.utils.get_popular_organization_slug,
                        unique=True,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DRAFT", "Draft"),
                            ("PLACEHOLDER", "Placeholder"),
                            ("PENDING", "Pending"),
                            ("ACTIVE", "Active"),
                            ("HIDDEN", "Hidden"),
                            ("REMOVED", "Removed"),
                        ],
                        default="ACTIVE",
                        max_length=20,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accountio.organization",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
    ]