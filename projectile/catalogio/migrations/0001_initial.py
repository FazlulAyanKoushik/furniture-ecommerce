# Generated by Django 4.1.3 on 2022-12-27 02:41

import autoslug.fields
import catalogio.paths
import catalogio.slugifiers
import dirtyfields.dirtyfields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accountio', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=catalogio.slugifiers.get_product_slug, unique=True)),
                ('description', models.TextField(blank=True)),
                ('seo_title', models.CharField(blank=True, max_length=100, verbose_name='SEO Title')),
                ('seo_description', models.TextField(blank=True, verbose_name='SEO Description')),
                ('image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=catalogio.paths.get_product_image_path)),
                ('sku', models.CharField(blank=True, max_length=100, verbose_name='SKU')),
                ('identifier', models.CharField(blank=True, max_length=40, null=True)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PUBLISHED', 'Published'), ('UNPUBLISHED', 'Unpublished'), ('ARCHIVED', 'Archived'), ('HIDDEN', 'Hidden'), ('REMOVED', 'Removed')], max_length=50)),
                ('published_at', models.DateTimeField(blank=True, null=True, verbose_name='Published At')),
                ('display_title', models.CharField(blank=True, max_length=100, verbose_name='Display Title')),
                ('like_count', models.PositiveIntegerField(default=0)),
                ('view_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('-created_at',),
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProductBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=catalogio.slugifiers.get_brand_slug, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=catalogio.paths.get_brand_image_path)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountio.organization')),
            ],
            options={
                'ordering': ('-created_at',),
                'unique_together': {('title', 'organization')},
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProductCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=catalogio.slugifiers.get_collection_slug, unique=True)),
                ('kind', models.CharField(choices=[('COLLECTION', 'Collection'), ('CATEGORY', 'Category')], db_index=True, max_length=20)),
                ('visibility', models.CharField(choices=[('PRIVATE', 'Private'), ('PUBLIC', 'Public')], db_index=True, max_length=20)),
                ('product_count', models.PositiveIntegerField(default=0)),
                ('image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=catalogio.paths.get_productcollection_image_path)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountio.organization')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogio.productcollection')),
            ],
            options={
                'ordering': ('-created_at',),
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProductView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogio.productbrand')),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogio.productcollection')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountio.organization')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalogio.product')),
            ],
            options={
                'ordering': ('-created_at',),
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=catalogio.paths.get_productimage_image_path)),
                ('width', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
                ('caption', models.CharField(blank=True, max_length=100, null=True)),
                ('copyright', models.CharField(blank=True, max_length=100, null=True)),
                ('priority', models.BigIntegerField(default=0)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountio.organization')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogio.product')),
            ],
            options={
                'ordering': ('-created_at',),
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProductCollectionBridge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogio.productcollection')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogio.product')),
            ],
            options={
                'unique_together': {('collection', 'product')},
                'index_together': {('collection', 'product')},
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.AddField(
            model_name='productcollection',
            name='products',
            field=models.ManyToManyField(through='catalogio.ProductCollectionBridge', to='catalogio.product'),
        ),
        migrations.CreateModel(
            name='ProductAsset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='')),
                ('extension', models.CharField(blank=True, max_length=50, null=True)),
                ('priority', models.BigIntegerField(default=0)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountio.organization')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogio.product')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='catalogio.productbrand'),
        ),
        migrations.AddField(
            model_name='product',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountio.organization'),
        ),
        migrations.CreateModel(
            name='HistoricalProductImage',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('image', models.TextField(blank=True, max_length=100, null=True)),
                ('width', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
                ('caption', models.CharField(blank=True, max_length=100, null=True)),
                ('copyright', models.CharField(blank=True, max_length=100, null=True)),
                ('priority', models.BigIntegerField(default=0)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accountio.organization')),
                ('product', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='catalogio.product')),
            ],
            options={
                'verbose_name': 'historical product image',
                'verbose_name_plural': 'historical product images',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalProductCollection',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('title', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=catalogio.slugifiers.get_collection_slug)),
                ('kind', models.CharField(choices=[('COLLECTION', 'Collection'), ('CATEGORY', 'Category')], db_index=True, max_length=20)),
                ('visibility', models.CharField(choices=[('PRIVATE', 'Private'), ('PUBLIC', 'Public')], db_index=True, max_length=20)),
                ('product_count', models.PositiveIntegerField(default=0)),
                ('image', models.TextField(blank=True, max_length=100, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accountio.organization')),
                ('parent', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='catalogio.productcollection')),
            ],
            options={
                'verbose_name': 'historical product collection',
                'verbose_name_plural': 'historical product collections',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalProductBrand',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('title', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=catalogio.slugifiers.get_brand_slug)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.TextField(blank=True, max_length=100, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accountio.organization')),
            ],
            options={
                'verbose_name': 'historical product brand',
                'verbose_name_plural': 'historical product brands',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalProductAsset',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('title', models.CharField(max_length=50)),
                ('file', models.TextField(max_length=100)),
                ('extension', models.CharField(blank=True, max_length=50, null=True)),
                ('priority', models.BigIntegerField(default=0)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accountio.organization')),
                ('product', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='catalogio.product')),
            ],
            options={
                'verbose_name': 'historical product asset',
                'verbose_name_plural': 'historical product assets',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalProduct',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('title', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=catalogio.slugifiers.get_product_slug)),
                ('description', models.TextField(blank=True)),
                ('seo_title', models.CharField(blank=True, max_length=100, verbose_name='SEO Title')),
                ('seo_description', models.TextField(blank=True, verbose_name='SEO Description')),
                ('image', models.TextField(blank=True, max_length=100, null=True)),
                ('sku', models.CharField(blank=True, max_length=100, verbose_name='SKU')),
                ('identifier', models.CharField(blank=True, max_length=40, null=True)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PUBLISHED', 'Published'), ('UNPUBLISHED', 'Unpublished'), ('ARCHIVED', 'Archived'), ('HIDDEN', 'Hidden'), ('REMOVED', 'Removed')], max_length=50)),
                ('published_at', models.DateTimeField(blank=True, null=True, verbose_name='Published At')),
                ('display_title', models.CharField(blank=True, max_length=100, verbose_name='Display Title')),
                ('like_count', models.PositiveIntegerField(default=0)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('brand', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='catalogio.productbrand')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accountio.organization')),
            ],
            options={
                'verbose_name': 'historical product',
                'verbose_name_plural': 'historical products',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
