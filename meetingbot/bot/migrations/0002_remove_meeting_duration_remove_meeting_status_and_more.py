# Generated by Django 5.1.4 on 2024-12-10 06:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='status',
        ),
        migrations.AddField(
            model_name='meeting',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
