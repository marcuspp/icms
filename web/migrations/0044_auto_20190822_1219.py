# Generated by Django 2.2.4 on 2019-08-22 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0043_auto_20190822_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessrequest',
            name='organisation_address',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
