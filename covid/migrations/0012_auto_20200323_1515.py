# Generated by Django 3.0.4 on 2020-03-23 15:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0011_auto_20200323_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coviddatamodel',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 23, 15, 15, 29, 598461), verbose_name='Last Update'),
        ),
        migrations.AlterField(
            model_name='statemodel',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2011, 11, 4, 0, 5, 23, 283000, tzinfo=utc), verbose_name='Last Update'),
        ),
    ]