# Generated by Django 3.0.4 on 2020-03-25 11:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0006_auto_20200324_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='countrymodel',
            name='new_cases',
            field=models.IntegerField(default=0, null=True, verbose_name='New Cases'),
        ),
        migrations.AlterField(
            model_name='coviddatamodel',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 25, 11, 52, 20, 338063, tzinfo=utc), verbose_name='Last Update'),
        ),
    ]
