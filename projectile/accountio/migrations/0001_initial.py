# Generated by Django 4.1.3 on 2023-01-12 21:12

import accountio.utils
import autoslug.fields
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
    ]

    operations = [
        migrations.CreateModel(
            name='Descendant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('display_name', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=accountio.utils.get_organization_slug, unique=True)),
                ('registration_no', models.CharField(blank=True, max_length=50)),
                ('address', models.TextField(blank=True)),
                ('postal_code', models.CharField(blank=True, max_length=50)),
                ('postal_area', models.CharField(blank=True, max_length=50)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('country', models.CharField(choices=[('af', 'Afghanistan\t '), ('al', 'Albania'), ('dz', 'Algeria'), ('as', 'American Samoa'), ('ad', 'Andorra'), ('ao', 'Angola'), ('ai', 'Anguilla'), ('aq', 'Antarctica'), ('ag', 'Antigua and Barbuda'), ('ar', 'Argentina'), ('am', 'Armenia'), ('aw', 'Aruba'), ('ac', 'Ascension Island'), ('au', 'Australia'), ('at', 'Austria'), ('az', 'Azerbaijan'), ('bs', 'Bahamas'), ('bh', 'Bahrain'), ('bd', 'Bangladesh'), ('bb', 'Barbados'), ('by', 'Belarus'), ('be', 'Belgium'), ('bz', 'Belize'), ('bj', 'Benin'), ('bm', 'Bermuda'), ('bt', 'Bhutan'), ('bo', 'Bolivia'), ('ba', 'Bosnia and Herzegovina'), ('bw', 'Botswana'), ('bv', 'Bouvet Island'), ('br', 'Brazil'), ('io', 'British Indian Ocean Territory'), ('vg', 'British Virgin Islands'), ('bn', 'Brunei Darussalam'), ('bg', 'Bulgaria'), ('bf', 'Burkina Faso'), ('bi', 'Burundi'), ('kh', 'Cambodia (Khmer)'), ('cm', 'Cameroon'), ('ca', 'Canada'), ('cv', 'Cape Verde'), ('ky', 'Cayman Islands'), ('cf', 'Central African Republic'), ('td', 'Chad'), ('cl', 'Chile'), ('cx', 'Christmas Island'), ('cc', 'Cocos (Keeling) Islands'), ('co', 'Colombia'), ('km', 'Comoros'), ('ck', 'Cook Islands'), ('cr', 'Costa Rica'), ('hr', 'Croatia (Hrvatska)'), ('cu', 'Cuba'), ('cy', 'Cyprus'), ('cz', 'Czech Republic'), ('ci', "Côte d'Ivoire"), ('cd', 'Democratic Republic of the Congo (Formerly Zaire)'), ('dk', 'Denmark'), ('dj', 'Djibouti'), ('dm', 'Dominica'), ('do', 'Dominican Republic'), ('tp', 'East Timor'), ('ec', 'Ecuador'), ('eg', 'Egypt'), ('sv', 'El Salvador'), ('gq', 'Equatorial Guinea'), ('er', 'Eritrea'), ('ee', 'Estonia'), ('et', 'Ethiopia'), ('eu', 'European Union'), ('fk', 'Falkland Islands'), ('fo', 'Faroe Islands'), ('fm', 'Federated States of Micronesia'), ('fj', 'Fiji'), ('fi', 'Finland'), ('fr', 'France'), ('gf', 'French Guiana'), ('pF', 'French Polynesia With Clipperton Island'), ('tf', 'French Southern and Antarctic Lands'), ('ga', 'Gabon'), ('ge', 'Georgia'), ('de', 'Germany (Deutschland)'), ('gh', 'Ghana'), ('gi', 'Gibraltar'), ('gr', 'Greece'), ('gl', 'Greenland'), ('gd', 'Grenada'), ('gp', 'Guadeloupe'), ('gu', 'Guam'), ('gt', 'Guatemala'), ('gg', 'Guernsey'), ('gn', 'Guinea'), ('gw', 'Guinea-Bissau'), ('gy', 'Guyana'), ('ht', 'Haiti'), ('hm', 'Heard Island and McDonald Islands'), ('hn', 'Honduras'), ('hk', 'Hong Kong'), ('hu', 'Hungary'), ('is', 'Iceland'), ('in', 'India'), ('id', 'Indonesia'), ('ir', 'Iran'), ('iq', 'Iraq'), ('ie', 'Ireland'), ('im', 'Isle of Man'), ('il', 'Israel'), ('it', 'Italy'), ('jm', 'Jamaica'), ('jp', 'Japan'), ('je', 'Jersey'), ('jo', 'Jordan'), ('kz', 'Kazakhstan'), ('ke', 'Kenya'), ('ki', 'Kiribati'), ('kw', 'Kuwait'), ('kg', 'Kyrgyzstan'), ('la', 'Laos'), ('lv', 'Latvia'), ('lb', 'Lebanon'), ('ls', 'Lesotho'), ('lr', 'Liberia'), ('ly', 'Libya'), ('li', 'Liechtenstein'), ('lt', 'Lithuania'), ('lu', 'Luxembourg'), ('mo', 'Macau'), ('mg', 'Madagascar'), ('mW', 'Malawi'), ('my', 'Malaysia'), ('mv', 'Maldives'), ('ml', 'Mali'), ('mt', 'Malta'), ('mh', 'Marshall Islands'), ('mq', 'Martinique'), ('mr', 'Mauritania'), ('mu', 'Mauritius'), ('yt', 'Mayotte'), ('mx', 'Mexico'), ('md', 'Moldova'), ('mc', 'Monaco'), ('mn', 'Mongolia'), ('me', 'Montenegro'), ('ms', 'Montserrat'), ('ma', 'Morocco'), ('mz', 'Mozambique'), ('mm', 'Myanmar'), ('na', 'Namibia'), ('nr', 'Nauru'), ('np', 'Nepal'), ('nl', 'Netherlands'), ('an', 'Netherlands Antilles'), ('nc', 'New Caledonia'), ('nz', 'New Zealand'), ('ni', 'Nicaragua'), ('ne', 'Niger'), ('ng', 'Nigeria'), ('nu', 'Niue'), ('nF', 'Norfolk Island'), ('mp', 'Northern Mariana Islands'), ('no', 'Norway'), ('om', 'Oman'), ('pk', 'Pakistan'), ('pw', 'Palau'), ('ps', 'Palestinian territories\tie, West Bank and Gaza Strip'), ('pa', 'Panama'), ('pg', 'Papua New Guinea'), ('py', 'Paraguay'), ('cn', "People's Republic of China"), ('pe', 'Peru'), ('ph', 'Philippines'), ('pn', 'Pitcairn Islands'), ('pl', 'Poland'), ('pt', 'Portugal'), ('pr', 'Puerto Rico'), ('qa', 'Qatar'), ('mk', 'Republic of Macedonia'), ('cg', 'Republic of the Congo'), ('ro', 'Romania'), ('ru', 'Russia'), ('rw', 'Rwanda'), ('re', 'Réunion'), ('sh', 'Saint Helena'), ('kn', 'Saint Kitts and Nevis'), ('lc', 'Saint Lucia'), ('vc', 'Saint Vincent and the Grenadines'), ('pm', 'Saint-Pierre and Miquelon'), ('ws', 'Samoa (Formerly Western Samoa)'), ('sm', 'San Marino'), ('sa', 'Saudi Arabia'), ('sn', 'Senegal'), ('rs', 'Serbia'), ('sc', 'Seychelles'), ('sl', 'Sierra Leone'), ('sg', 'Singapore'), ('sk', 'Slovakia'), ('si', 'Slovenia'), ('sb', 'Solomon Islands'), ('so', 'Somalia'), ('za', 'South Africa'), ('gs', 'South Georgia and the South Sandwich Islands'), ('kr', 'South Korea'), ('su', 'Soviet Union'), ('es', 'Spain (España)'), ('lk', 'Sri Lanka'), ('sd', 'Sudan'), ('sr', 'Suriname'), ('sj', 'Svalbard and Jan Mayen Islands'), ('sz', 'Swaziland'), ('se', 'Sweden'), ('ch', 'Switzerland'), ('sy', 'Syria'), ('st', 'São Tomé and Príncipe'), ('tw', 'Taiwan'), ('tj', 'Tajikistan'), ('tz', 'Tanzania'), ('th', 'Thailand'), ('gm', 'The Gambia'), ('tl', 'Timor-Leste'), ('tg', 'Togo'), ('tk', 'Tokelau'), ('to', 'Tonga'), ('tt', 'Trinidad and Tobago'), ('tn', 'Tunisia'), ('tr', 'Turkey'), ('tm', 'Turkmenistan'), ('tc', 'Turks and Caicos Islands'), ('tv', 'Tuvalu'), ('vi', 'US Virgin Islands'), ('ug', 'Uganda'), ('ua', 'Ukraine'), ('ae', 'United Arab Emirates'), ('gb', 'United Kingdom'), ('uk', 'United Kingdom'), ('um', 'United States Minor Outlying Islands'), ('us', 'United States of America'), ('uy', 'Uruguay'), ('uz', 'Uzbekistan'), ('vu', 'Vanuatu'), ('va', 'Vatican City State'), ('ve', 'Venezuela'), ('vn', 'Vietnam'), ('wf', 'Wallis and Futuna'), ('ye', 'Yemen'), ('yu', 'Yugoslavia'), ('zm', 'Zambia'), ('zw', 'Zimbabwe')], db_index=True, default='se', max_length=2)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('website_url', models.URLField(blank=True)),
                ('blog_url', models.URLField(blank=True)),
                ('linkedin_url', models.URLField(blank=True)),
                ('instagram_url', models.URLField(blank=True)),
                ('facebook_url', models.URLField(blank=True)),
                ('twitter_url', models.URLField(blank=True)),
                ('size', models.CharField(choices=[('ZERO_TO_ONE', '0-1 employees'), ('TWO_TO_TEN', '2-10 employees'), ('ELEVEN_TO_FIFTY', '11-50 employees'), ('FIFTY_ONE_PLUS', '51-200 employees'), ('TWO_HUNDRED_PLUS', '201-500 employees'), ('FIVE_HUNDRED_PLUS', '501-1,000 employees'), ('ONE_THOUSAND_PLUS', '1,001-5,000 employees'), ('FIVE_THOUSAND_PLUS', '5,001-10,000 employees'), ('TEN_THOUSAND_PLUS', '10,001+ employees')], default='ZERO_TO_ONE', max_length=20)),
                ('summary', models.TextField(blank=True, help_text='Short summary about company.')),
                ('description', models.TextField(blank=True, help_text='Longer description about company.')),
                ('kind', models.CharField(choices=[('UNKNOWN', 'Unknown'), ('SUPPLIER', 'Supplier'), ('RETAILER', 'Retailer'), ('ARCHITECT', 'Architect'), ('INTERIOR_DESIGNER', 'Interior Designer'), ('FURNITURE_DESIGNER', 'Furniture Designer'), ('PROJECT_MANAGER', 'Project Manager'), ('CARPENTER', 'Carpenter'), ('PAINTER', 'Painter'), ('TAILOR', 'Tailor'), ('ELECTRICIAN', 'Electrician'), ('PLUMBER', 'Plumber'), ('OTHER', 'Other')], db_index=True, max_length=20)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PENDING', 'Pending'), ('ACTIVE', 'Active'), ('HIDDEN', 'Hidden'), ('REMOVED', 'Removed')], db_index=True, default='DRAFT', max_length=20)),
                ('avatar', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=accountio.utils.get_organization_media_path_prefix)),
                ('hero', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=accountio.utils.get_organization_media_path_prefix)),
                ('logo_wide', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=accountio.utils.get_organization_media_path_prefix)),
                ('image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=accountio.utils.get_organization_media_path_prefix)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='accountio.organization')),
                ('parents', models.ManyToManyField(through='accountio.Descendant', to='accountio.organization')),
            ],
            options={
                'ordering': ('-created_at',),
                'unique_together': {('registration_no', 'country')},
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalOrganization',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('display_name', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=accountio.utils.get_organization_slug)),
                ('registration_no', models.CharField(blank=True, max_length=50)),
                ('address', models.TextField(blank=True)),
                ('postal_code', models.CharField(blank=True, max_length=50)),
                ('postal_area', models.CharField(blank=True, max_length=50)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('country', models.CharField(choices=[('af', 'Afghanistan\t '), ('al', 'Albania'), ('dz', 'Algeria'), ('as', 'American Samoa'), ('ad', 'Andorra'), ('ao', 'Angola'), ('ai', 'Anguilla'), ('aq', 'Antarctica'), ('ag', 'Antigua and Barbuda'), ('ar', 'Argentina'), ('am', 'Armenia'), ('aw', 'Aruba'), ('ac', 'Ascension Island'), ('au', 'Australia'), ('at', 'Austria'), ('az', 'Azerbaijan'), ('bs', 'Bahamas'), ('bh', 'Bahrain'), ('bd', 'Bangladesh'), ('bb', 'Barbados'), ('by', 'Belarus'), ('be', 'Belgium'), ('bz', 'Belize'), ('bj', 'Benin'), ('bm', 'Bermuda'), ('bt', 'Bhutan'), ('bo', 'Bolivia'), ('ba', 'Bosnia and Herzegovina'), ('bw', 'Botswana'), ('bv', 'Bouvet Island'), ('br', 'Brazil'), ('io', 'British Indian Ocean Territory'), ('vg', 'British Virgin Islands'), ('bn', 'Brunei Darussalam'), ('bg', 'Bulgaria'), ('bf', 'Burkina Faso'), ('bi', 'Burundi'), ('kh', 'Cambodia (Khmer)'), ('cm', 'Cameroon'), ('ca', 'Canada'), ('cv', 'Cape Verde'), ('ky', 'Cayman Islands'), ('cf', 'Central African Republic'), ('td', 'Chad'), ('cl', 'Chile'), ('cx', 'Christmas Island'), ('cc', 'Cocos (Keeling) Islands'), ('co', 'Colombia'), ('km', 'Comoros'), ('ck', 'Cook Islands'), ('cr', 'Costa Rica'), ('hr', 'Croatia (Hrvatska)'), ('cu', 'Cuba'), ('cy', 'Cyprus'), ('cz', 'Czech Republic'), ('ci', "Côte d'Ivoire"), ('cd', 'Democratic Republic of the Congo (Formerly Zaire)'), ('dk', 'Denmark'), ('dj', 'Djibouti'), ('dm', 'Dominica'), ('do', 'Dominican Republic'), ('tp', 'East Timor'), ('ec', 'Ecuador'), ('eg', 'Egypt'), ('sv', 'El Salvador'), ('gq', 'Equatorial Guinea'), ('er', 'Eritrea'), ('ee', 'Estonia'), ('et', 'Ethiopia'), ('eu', 'European Union'), ('fk', 'Falkland Islands'), ('fo', 'Faroe Islands'), ('fm', 'Federated States of Micronesia'), ('fj', 'Fiji'), ('fi', 'Finland'), ('fr', 'France'), ('gf', 'French Guiana'), ('pF', 'French Polynesia With Clipperton Island'), ('tf', 'French Southern and Antarctic Lands'), ('ga', 'Gabon'), ('ge', 'Georgia'), ('de', 'Germany (Deutschland)'), ('gh', 'Ghana'), ('gi', 'Gibraltar'), ('gr', 'Greece'), ('gl', 'Greenland'), ('gd', 'Grenada'), ('gp', 'Guadeloupe'), ('gu', 'Guam'), ('gt', 'Guatemala'), ('gg', 'Guernsey'), ('gn', 'Guinea'), ('gw', 'Guinea-Bissau'), ('gy', 'Guyana'), ('ht', 'Haiti'), ('hm', 'Heard Island and McDonald Islands'), ('hn', 'Honduras'), ('hk', 'Hong Kong'), ('hu', 'Hungary'), ('is', 'Iceland'), ('in', 'India'), ('id', 'Indonesia'), ('ir', 'Iran'), ('iq', 'Iraq'), ('ie', 'Ireland'), ('im', 'Isle of Man'), ('il', 'Israel'), ('it', 'Italy'), ('jm', 'Jamaica'), ('jp', 'Japan'), ('je', 'Jersey'), ('jo', 'Jordan'), ('kz', 'Kazakhstan'), ('ke', 'Kenya'), ('ki', 'Kiribati'), ('kw', 'Kuwait'), ('kg', 'Kyrgyzstan'), ('la', 'Laos'), ('lv', 'Latvia'), ('lb', 'Lebanon'), ('ls', 'Lesotho'), ('lr', 'Liberia'), ('ly', 'Libya'), ('li', 'Liechtenstein'), ('lt', 'Lithuania'), ('lu', 'Luxembourg'), ('mo', 'Macau'), ('mg', 'Madagascar'), ('mW', 'Malawi'), ('my', 'Malaysia'), ('mv', 'Maldives'), ('ml', 'Mali'), ('mt', 'Malta'), ('mh', 'Marshall Islands'), ('mq', 'Martinique'), ('mr', 'Mauritania'), ('mu', 'Mauritius'), ('yt', 'Mayotte'), ('mx', 'Mexico'), ('md', 'Moldova'), ('mc', 'Monaco'), ('mn', 'Mongolia'), ('me', 'Montenegro'), ('ms', 'Montserrat'), ('ma', 'Morocco'), ('mz', 'Mozambique'), ('mm', 'Myanmar'), ('na', 'Namibia'), ('nr', 'Nauru'), ('np', 'Nepal'), ('nl', 'Netherlands'), ('an', 'Netherlands Antilles'), ('nc', 'New Caledonia'), ('nz', 'New Zealand'), ('ni', 'Nicaragua'), ('ne', 'Niger'), ('ng', 'Nigeria'), ('nu', 'Niue'), ('nF', 'Norfolk Island'), ('mp', 'Northern Mariana Islands'), ('no', 'Norway'), ('om', 'Oman'), ('pk', 'Pakistan'), ('pw', 'Palau'), ('ps', 'Palestinian territories\tie, West Bank and Gaza Strip'), ('pa', 'Panama'), ('pg', 'Papua New Guinea'), ('py', 'Paraguay'), ('cn', "People's Republic of China"), ('pe', 'Peru'), ('ph', 'Philippines'), ('pn', 'Pitcairn Islands'), ('pl', 'Poland'), ('pt', 'Portugal'), ('pr', 'Puerto Rico'), ('qa', 'Qatar'), ('mk', 'Republic of Macedonia'), ('cg', 'Republic of the Congo'), ('ro', 'Romania'), ('ru', 'Russia'), ('rw', 'Rwanda'), ('re', 'Réunion'), ('sh', 'Saint Helena'), ('kn', 'Saint Kitts and Nevis'), ('lc', 'Saint Lucia'), ('vc', 'Saint Vincent and the Grenadines'), ('pm', 'Saint-Pierre and Miquelon'), ('ws', 'Samoa (Formerly Western Samoa)'), ('sm', 'San Marino'), ('sa', 'Saudi Arabia'), ('sn', 'Senegal'), ('rs', 'Serbia'), ('sc', 'Seychelles'), ('sl', 'Sierra Leone'), ('sg', 'Singapore'), ('sk', 'Slovakia'), ('si', 'Slovenia'), ('sb', 'Solomon Islands'), ('so', 'Somalia'), ('za', 'South Africa'), ('gs', 'South Georgia and the South Sandwich Islands'), ('kr', 'South Korea'), ('su', 'Soviet Union'), ('es', 'Spain (España)'), ('lk', 'Sri Lanka'), ('sd', 'Sudan'), ('sr', 'Suriname'), ('sj', 'Svalbard and Jan Mayen Islands'), ('sz', 'Swaziland'), ('se', 'Sweden'), ('ch', 'Switzerland'), ('sy', 'Syria'), ('st', 'São Tomé and Príncipe'), ('tw', 'Taiwan'), ('tj', 'Tajikistan'), ('tz', 'Tanzania'), ('th', 'Thailand'), ('gm', 'The Gambia'), ('tl', 'Timor-Leste'), ('tg', 'Togo'), ('tk', 'Tokelau'), ('to', 'Tonga'), ('tt', 'Trinidad and Tobago'), ('tn', 'Tunisia'), ('tr', 'Turkey'), ('tm', 'Turkmenistan'), ('tc', 'Turks and Caicos Islands'), ('tv', 'Tuvalu'), ('vi', 'US Virgin Islands'), ('ug', 'Uganda'), ('ua', 'Ukraine'), ('ae', 'United Arab Emirates'), ('gb', 'United Kingdom'), ('uk', 'United Kingdom'), ('um', 'United States Minor Outlying Islands'), ('us', 'United States of America'), ('uy', 'Uruguay'), ('uz', 'Uzbekistan'), ('vu', 'Vanuatu'), ('va', 'Vatican City State'), ('ve', 'Venezuela'), ('vn', 'Vietnam'), ('wf', 'Wallis and Futuna'), ('ye', 'Yemen'), ('yu', 'Yugoslavia'), ('zm', 'Zambia'), ('zw', 'Zimbabwe')], db_index=True, default='se', max_length=2)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('website_url', models.URLField(blank=True)),
                ('blog_url', models.URLField(blank=True)),
                ('linkedin_url', models.URLField(blank=True)),
                ('instagram_url', models.URLField(blank=True)),
                ('facebook_url', models.URLField(blank=True)),
                ('twitter_url', models.URLField(blank=True)),
                ('size', models.CharField(choices=[('ZERO_TO_ONE', '0-1 employees'), ('TWO_TO_TEN', '2-10 employees'), ('ELEVEN_TO_FIFTY', '11-50 employees'), ('FIFTY_ONE_PLUS', '51-200 employees'), ('TWO_HUNDRED_PLUS', '201-500 employees'), ('FIVE_HUNDRED_PLUS', '501-1,000 employees'), ('ONE_THOUSAND_PLUS', '1,001-5,000 employees'), ('FIVE_THOUSAND_PLUS', '5,001-10,000 employees'), ('TEN_THOUSAND_PLUS', '10,001+ employees')], default='ZERO_TO_ONE', max_length=20)),
                ('summary', models.TextField(blank=True, help_text='Short summary about company.')),
                ('description', models.TextField(blank=True, help_text='Longer description about company.')),
                ('kind', models.CharField(choices=[('UNKNOWN', 'Unknown'), ('SUPPLIER', 'Supplier'), ('RETAILER', 'Retailer'), ('ARCHITECT', 'Architect'), ('INTERIOR_DESIGNER', 'Interior Designer'), ('FURNITURE_DESIGNER', 'Furniture Designer'), ('PROJECT_MANAGER', 'Project Manager'), ('CARPENTER', 'Carpenter'), ('PAINTER', 'Painter'), ('TAILOR', 'Tailor'), ('ELECTRICIAN', 'Electrician'), ('PLUMBER', 'Plumber'), ('OTHER', 'Other')], db_index=True, max_length=20)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PENDING', 'Pending'), ('ACTIVE', 'Active'), ('HIDDEN', 'Hidden'), ('REMOVED', 'Removed')], db_index=True, default='DRAFT', max_length=20)),
                ('avatar', models.TextField(blank=True, max_length=100, null=True)),
                ('hero', models.TextField(blank=True, max_length=100, null=True)),
                ('logo_wide', models.TextField(blank=True, max_length=100, null=True)),
                ('image', models.TextField(blank=True, max_length=100, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accountio.organization')),
            ],
            options={
                'verbose_name': 'historical organization',
                'verbose_name_plural': 'historical organizations',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddField(
            model_name='descendant',
            name='child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_set', to='accountio.organization'),
        ),
        migrations.AddField(
            model_name='descendant',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='descendant_set', to='accountio.organization'),
        ),
        migrations.CreateModel(
            name='OrganizationUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role', models.CharField(choices=[('INITIATOR', 'Initiator'), ('STAFF', 'Staff'), ('ADMIN', 'Admin'), ('OWNER', 'Owner')], max_length=20)),
                ('status', models.CharField(choices=[('INVITED', 'Invited'), ('PENDING', 'Pending'), ('ACTIVE', 'Active'), ('REJECTED', 'Rejected'), ('HIDDEN', 'Hidden'), ('REMOVED', 'Removed')], db_index=True, default='PENDING', max_length=20)),
                ('is_default', models.BooleanField(default=False)),
                ('token', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True)),
                ('reminded_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountio.organization')),
                ('referrer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accountio.organizationuser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Organization Users',
                'ordering': ('created_at',),
                'unique_together': {('organization', 'user')},
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='descendant',
            unique_together={('parent', 'child')},
        ),
        migrations.AlterIndexTogether(
            name='descendant',
            index_together={('parent', 'child')},
        ),
    ]