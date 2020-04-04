# Generated by Django 3.0.4 on 2020-04-04 15:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0011_auto_20200404_0636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newcoviddatamodel',
            name='country',
        ),
        migrations.DeleteModel(
            name='NewFetchedDataFiles',
        ),
        migrations.AlterField(
            model_name='coviddatamodel',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 4, 15, 20, 36, 96984, tzinfo=utc), verbose_name='Last Update'),
        ),
        migrations.DeleteModel(
            name='NewCountryModel',
        ),
        migrations.DeleteModel(
            name='NewCovidDataModel',
        ),
    ]
