# Generated by Django 4.1.7 on 2023-05-12 09:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalogio", "0007_productdiscount_amount_productdiscount_currency_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="productdiscount",
            options={"ordering": ("-created_at",)},
        ),
    ]