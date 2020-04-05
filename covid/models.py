from django.db import models
import datetime

from django.db.models import Sum, F, Count, Max
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def get_time():
    return datetime.date(2000, 1, 1)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days+1)):
        yield start_date + datetime.timedelta(n)


# Create your models here.
class CountryModel(models.Model):
    country = models.CharField(_('Country'), max_length=70, null=False)
    latest_confirmed_cases = models.IntegerField(default=0)
    latest_deaths = models.IntegerField(default=0)
    latest_recovered = models.IntegerField(default=0)
    last_updated = models.DateField(_('Last Update Day'), default=get_time(), null=False)

    def __str__(self):
        return f"{self.country}"

    @classmethod
    def get_all_latest_country_total(cls):
        return CountryModel.objects.all().values('country').annotate(
            confirmed_cases=Max('coviddatamodel__confirmed_cases'),
            deaths=Max('coviddatamodel__deaths'),
            recovered=Max('coviddatamodel__recovered')).values(
            'country', 'confirmed_cases', 'deaths', 'recovered').order_by('-confirmed_cases')

    @classmethod
    def get_total_data(cls):
        confirmed_cases = 0
        deaths = 0
        recovered = 0
        latest_date = CovidDataModel.objects.all().order_by('-date').first().date
        for each in CovidDataModel.objects.filter(date=latest_date):
            confirmed_cases += each.confirmed_cases
            deaths += each.deaths
            recovered += each.recovered
        death_percent = round((deaths / confirmed_cases * 100), 2)
        recovered_percent = round((recovered / confirmed_cases * 100), 2)
        return {"cases": confirmed_cases, "deaths": deaths, "recovered": recovered, "date": latest_date,
                'deaths_percent': death_percent, 'recovered_percent': recovered_percent}

    @classmethod
    def get_bar_graph_data(cls):
        ordered_queryset = CovidDataModel.objects.all().order_by('-date')
        start_date = ordered_queryset.last().date
        end_date = ordered_queryset.first().date
        cases_data = []
        deaths_data = []
        recovered_data = []
        for date in daterange(start_date, end_date):
            confirmed_cases = 0
            deaths = 0
            recovered = 0
            for each in CovidDataModel.objects.filter(date=date):
                confirmed_cases += each.confirmed_cases
                deaths += each.deaths
                recovered += each.recovered
            cases_data.append({'date': date, 'cases': confirmed_cases})
            deaths_data.append({'date': date, 'deaths': deaths})
            recovered_data.append({'date': date, 'recovered': recovered})
        return cases_data, deaths_data, recovered_data

    @classmethod
    def get_total_data_timeline(cls):
        timeline_data = {}
        ordered_queryset = CovidDataModel.objects.all().order_by('-date')
        start_date = ordered_queryset.last().date
        end_date = ordered_queryset.first().date
        for date in daterange(start_date, end_date):
            data = []
            for each in CountryModel.objects.filter(coviddatamodel__date=date).annotate(cases=F(
                    'coviddatamodel__confirmed_cases')).values('country', 'cases'):
                confirmed_cases = each['cases']
                country = each['country']
                data.append({'country': country, 'cases': confirmed_cases})
            timeline_data.update({str(date): data})

        return timeline_data


class CovidDataModel(models.Model):
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE, null=False)
    datetime = models.DateTimeField(_('Last Update'), default=timezone.now(), null=False)
    date = models.DateField(_('Last Update Day'), default=get_time(), null=False)
    confirmed_cases = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    recovered = models.IntegerField(default=0)

    def __str__(self):
        return f"{str(self.country) + '_' + str(self.date.year) + '_' + str(self.date.month) + '_' + str(self.date.day)}"


@receiver(post_save, sender=CovidDataModel)
def update_latest_values(**kwargs):
    instance = kwargs["instance"]
    get_country_model = CountryModel.objects.get(id=instance.country.id)
    if instance.date >= get_country_model.last_updated:
        get_country_model.latest_confirmed_cases = instance.confirmed_cases
        get_country_model.latest_deaths = instance.deaths
        get_country_model.latest_recovered = instance.recovered
        get_country_model.last_updated = instance.date
        get_country_model.save()


class FetchedDataFiles(models.Model):
    filename = models.CharField(max_length=400)

    def __str__(self):
        return f"{self.filename}"
