# Generated by Django 4.1.7 on 2023-08-09 04:51

import autoslug.fields
import catalogio.slugifiers
import dirtyfields.dirtyfields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accountio', '0006_organizationuser_designation'),
        ('catalogio', '0012_historicalproduct_channels_product_channels'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='organization',
        ),
        migrations.AddField(
            model_name='service',
            name='kind',
            field=models.CharField(choices=[('SERVICE', 'Service'), ('PRESET_SERVICE', 'Preset Service')], db_index=True, default='SERVICE', max_length=30),
        ),
        migrations.AddField(
            model_name='service',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='catalogio.service'),
        ),
        migrations.AddField(
            model_name='service',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='s', editable=False, populate_from=catalogio.slugifiers.get_service_slug, unique=True),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='OrganizationServiceConnector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountio.organization')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogio.service')),
            ],
            options={
                'ordering': ('-created_at',),
                'unique_together': {('organization', 'service')},
                'index_together': {('organization', 'service')},
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
    ]
