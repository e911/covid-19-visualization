from django.db import models
import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def get_time():
    return timezone.make_aware(datetime.datetime(2011, 11, 4, 0, 5, 23, 283000), timezone.get_default_timezone())


# Create your models here.
class CountryModel(models.Model):
    country = models.CharField(_('Country'), max_length=70, null=False)

    def __str__(self):
        return f"{self.country}"


class CityModel(models.Model):
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE, null=False)
    city = models.CharField(_('City'), max_length=70, null=True)
    latest_confirmed_cases = models.IntegerField(default=0)
    latest_deaths = models.IntegerField(default=0)
    latest_recovered = models.IntegerField(default=0)
    last_updated = models.DateTimeField(_('Last Update'), default=get_time(), null=False)

    def __str__(self):
        return f"{str(self.country) + '-' + self.city}"


class CovidDataModel(models.Model):
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE, null=False)
    city = models.ForeignKey(CityModel, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(_('Last Update'), default=datetime.datetime.now(), null=False)
    confirmed_cases = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    recovered = models.IntegerField(default=0)

    def __str__(self):
        return f"{str(self.city) + '_' + str(self.date.year) + '_' + str(self.date.month) + '_' + str(self.date.day)}"


@receiver(post_save, sender=CovidDataModel)
def update_latest_values(**kwargs):
    instance = kwargs["instance"]
    get_city_model = CityModel.objects.get(id=instance.city.id)
    if instance.date > get_city_model.last_updated:
        get_city_model.latest_confirmed_cases = instance.confirmed_cases
        get_city_model.latest_deaths = instance.deaths
        get_city_model.latest_recovered = instance.recovered
        get_city_model.last_updated = instance.date
        get_city_model.save()


class FetchedDataFiles(models.Model):
    filename = models.CharField(max_length=400)

    def __str__(self):
        return f"{self.filename}"
