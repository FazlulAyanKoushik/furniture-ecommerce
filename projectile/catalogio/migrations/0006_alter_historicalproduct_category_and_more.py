# Generated by Django 4.1.7 on 2023-04-03 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogio", "0005_alter_historicalproduct_scraped_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalproduct",
            name="category",
            field=models.CharField(blank=True, db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="historicalproduct",
            name="color",
            field=models.CharField(blank=True, db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="historicalproduct",
            name="material",
            field=models.CharField(blank=True, db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.CharField(blank=True, db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="product",
            name="color",
            field=models.CharField(blank=True, db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="product",
            name="material",
            field=models.CharField(blank=True, db_index=True, max_length=100),
        ),
    ]