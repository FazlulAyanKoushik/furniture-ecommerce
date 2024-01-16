# Generated by Django 4.1.7 on 2023-04-05 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogio', '0006_alter_historicalproduct_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdiscount',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=3, default=None, max_digits=19, null=True),
        ),
        migrations.AddField(
            model_name='productdiscount',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('DKK', 'DKK'), ('SEK', 'SEK'), ('NOK', 'NOK')], default='SEK', max_length=3),
        ),
        migrations.AddField(
            model_name='productdiscount',
            name='variant',
            field=models.CharField(choices=[('PRICE_LIST', 'Price List'), ('AMOUNT', 'Amount')], default='PRICE_LIST', max_length=20),
        ),
    ]
