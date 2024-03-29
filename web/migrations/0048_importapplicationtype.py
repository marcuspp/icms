# Generated by Django 2.2.4 on 2019-08-27 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0047_auto_20190825_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportApplicationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField()),
                ('type_code', models.CharField(max_length=30)),
                ('type', models.CharField(max_length=70)),
                ('sub_type_code', models.CharField(max_length=30)),
                ('sub_type', models.CharField(max_length=70)),
                ('licent_type_code', models.CharField(max_length=20)),
                ('sigl_flag', models.BooleanField()),
                ('chief_flag', models.BooleanField()),
                ('chief_license_prefix', models.CharField(blank=True, max_length=10, null=True)),
                ('paper_license_flag', models.BooleanField()),
                ('electronic_license_flag', models.BooleanField()),
                ('cover_letter_flag', models.BooleanField()),
                ('cover_letter_schedule_flag', models.BooleanField()),
                ('category_flag', models.BooleanField()),
                ('sigl_category_prefix', models.CharField(blank=True, max_length=100, null=True)),
                ('chief_category_prefix', models.CharField(blank=True, max_length=10, null=True)),
                ('default_license_length_months', models.IntegerField(blank=True, null=True)),
                ('endorsements_flag', models.BooleanField()),
                ('default_commodity_desc', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity_unlimited_flag', models.BooleanField()),
                ('unit_list_csv', models.CharField(blank=True, max_length=200, null=True)),
                ('exp_cert_upload_flag', models.BooleanField()),
                ('supporting_docs_upload_flag', models.BooleanField()),
                ('multiple_commodities_flag', models.BooleanField()),
                ('guidance_file_url', models.CharField(blank=True, max_length=4000, null=True)),
                ('license_category_description', models.CharField(blank=True, max_length=1000, null=True)),
                ('usage_auto_category_desc_flag', models.BooleanField()),
                ('case_checklist_flag', models.BooleanField()),
                ('importer_printable', models.BooleanField()),
                ('commodity_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='web.CommodityType')),
                ('consignment_country_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='application_types_to', to='web.CountryGroup')),
                ('declaration_template', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='web.Template')),
                ('default_commodity_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='web.CommodityGroup')),
                ('endorsements', models.ManyToManyField(to='web.Role')),
                ('master_country_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='application_types', to='web.CountryGroup')),
                ('origin_country_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='application_types_from', to='web.CountryGroup')),
            ],
        ),
    ]
