# Generated by Django 3.0.4 on 2020-03-23 15:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0012_auto_20200323_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coviddatamodel',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 23, 15, 22, 25, 107811), verbose_name='Last Update'),
        ),
    ]