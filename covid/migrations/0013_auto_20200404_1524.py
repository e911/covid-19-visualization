# Generated by Django 3.0.4 on 2020-04-04 15:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0012_auto_20200404_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coviddatamodel',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 4, 15, 24, 9, 30692, tzinfo=utc), verbose_name='Last Update'),
        ),
    ]
