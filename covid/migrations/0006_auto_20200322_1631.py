# Generated by Django 3.0.4 on 2020-03-22 16:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0005_auto_20200322_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coviddatamodel',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 22, 16, 31, 35, 297649), verbose_name='Last Update'),
        ),
    ]
