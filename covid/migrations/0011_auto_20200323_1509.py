# Generated by Django 3.0.4 on 2020-03-23 15:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0010_auto_20200323_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coviddatamodel',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 23, 15, 9, 8, 46466), verbose_name='Last Update'),
        ),
        migrations.AlterField(
            model_name='statemodel',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2011, 11, 4, 0, 5, 23), verbose_name='Last Update'),
        ),
    ]
