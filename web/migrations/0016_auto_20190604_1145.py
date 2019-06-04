# Generated by Django 2.2.1 on 2019-06-04 11:45

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('web', '0015_templates'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.Group')),
                ('description', models.CharField(blank=True, max_length=4000, null=True)),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.AlterModelOptions(
            name='template',
            options={'ordering': ('-is_active',)},
        ),
    ]