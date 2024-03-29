# Generated by Django 2.2.2 on 2019-08-14 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0033_auto_20190730_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='account_status',
            field=models.CharField(choices=[('NEW', 'NEW'), ('BLOCKED', 'Blocked'), ('SUSPENDED', 'Suspended'), ('CANCELLED', 'Cancelled'), ('ACTIVE', 'ACTIVE')], default='NEW', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='account_status_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_changed', to='web.User'),
        ),
        migrations.AddField(
            model_name='user',
            name='account_status_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='password_disposition',
            field=models.CharField(blank=True, choices=[('TEMPORARY', 'Temporary'), ('FULL', 'Full')], max_length=20, null=True),
        ),
    ]
