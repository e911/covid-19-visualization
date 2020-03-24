from django.db import models
import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def get_time():
    return datetime.date(2000,1,1)


# Create your models here.
class CountryModel(models.Model):
    country = models.CharField(_('Country'), max_length=70, null=False)
    latest_confirmed_cases = models.IntegerField(default=0)
    latest_deaths = models.IntegerField(default=0)
    latest_recovered = models.IntegerField(default=0)
    last_updated = models.DateField(_('Last Update Day'), default=get_time(), null=False)

    def __str__(self):
        return f"{self.country}"


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
