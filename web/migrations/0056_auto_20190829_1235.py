# Generated by Django 2.2.4 on 2019-08-29 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0055_auto_20190829_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='caseconstabularyemail',
            name='email_response',
            field=models.CharField(blank=True, max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='caseconstabularyemail',
            name='email_body',
            field=models.CharField(max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='caseconstabularyemail',
            name='email_subject',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
