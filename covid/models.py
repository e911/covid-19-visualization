from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CountryModel(models.Model):
    country = models.CharField(_('Country'), max_length=70, null=False)

    def __str__(self):
        return f"{self.country}"


class CovidDataModel(models.Model):
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE, null=False)
    state = models.CharField(_('State'), max_length=70, null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    date = models.DateTimeField(_('Last Update'), default=datetime.datetime.now(), null=False)
    confirmed_cases = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    recovered = models.IntegerField(default=0)

    def __str__(self):
        return f"{str(self.country) + str(self.state) + '_' + str(self.date.year) + '_' + str(self.date.month) + '_' + str(self.date.day)}"


class FetchedDataFiles(models.Model):
    filename = models.CharField(max_length=400)

    def __str__(self):
        return f"{self.filename}"
