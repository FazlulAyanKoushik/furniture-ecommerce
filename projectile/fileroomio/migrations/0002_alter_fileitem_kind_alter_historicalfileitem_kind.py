# Generated by Django 4.1.6 on 2023-02-15 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileroomio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileitem',
            name='kind',
            field=models.CharField(choices=[('IMAGE', 'Image'), ('VIDEO', 'Video'), ('PRICE_LIST', 'Price List'), ('BROCHURE', 'Brochure'), ('OTHER', 'Other')], max_length=20),
        ),
        migrations.AlterField(
            model_name='historicalfileitem',
            name='kind',
            field=models.CharField(choices=[('IMAGE', 'Image'), ('VIDEO', 'Video'), ('PRICE_LIST', 'Price List'), ('BROCHURE', 'Brochure'), ('OTHER', 'Other')], max_length=20),
        ),
    ]