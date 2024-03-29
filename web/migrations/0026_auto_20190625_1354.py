# Generated by Django 2.2.2 on 2019-06-25 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0024_auto_20190624_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductLegislation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('is_active', models.BooleanField(default=False)),
                ('is_biocidal', models.BooleanField(default=False)),
                ('is_eu_cosmetics_regulation', models.BooleanField(default=False)),
                ('is_biocidal_claim', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='countrygroup',
            name='countries',
            field=models.ManyToManyField(blank=True, related_name='country_groups', to='web.Country'),
        ),
    ]
