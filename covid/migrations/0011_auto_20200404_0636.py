# Generated by Django 3.0.4 on 2020-04-04 06:36

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0010_auto_20200329_0714'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewCountryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=70, verbose_name='Country')),
                ('latest_confirmed_cases', models.IntegerField(default=0)),
                ('latest_deaths', models.IntegerField(default=0)),
                ('latest_recovered', models.IntegerField(default=0)),
                ('last_updated', models.DateField(default=datetime.date(2000, 1, 1), verbose_name='Last Update Day')),
            ],
        ),
        migrations.CreateModel(
            name='NewFetchedDataFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=400)),
            ],
        ),
        migrations.AlterField(
            model_name='coviddatamodel',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 4, 6, 36, 48, 932218, tzinfo=utc), verbose_name='Last Update'),
        ),
        migrations.CreateModel(
            name='NewCovidDataModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=datetime.datetime(2020, 4, 4, 6, 36, 48, 934600, tzinfo=utc), verbose_name='Last Update')),
                ('date', models.DateField(default=datetime.date(2000, 1, 1), verbose_name='Last Update Day')),
                ('confirmed_cases', models.IntegerField(default=0)),
                ('deaths', models.IntegerField(default=0)),
                ('recovered', models.IntegerField(default=0)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covid.NewCountryModel')),
            ],
        ),
    ]