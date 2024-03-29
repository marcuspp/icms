# Generated by Django 2.1.8 on 2019-05-14 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.CharField(max_length=4000, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='job_title',
            field=models.CharField(max_length=320, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='location_at_address',
            field=models.CharField(max_length=4000, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='middle_initials',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='preferred_first_name',
            field=models.CharField(blank=True, max_length=4000, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='work_address',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='template',
            name='application_domain',
            field=models.CharField(choices=[('CA', 'Certificate Applications'), ('IMA', 'Import Applications'), ('IAR', 'Access Requests')], max_length=20),
        ),
    ]
