from django.contrib import admin
from covid.models import CountryModel, CovidDataModel, FetchedDataFiles


class CountryModelAdmin(admin.ModelAdmin):
    class Meta:
        model = CountryModel
        exclude = []


class CovidDataModelAdmin(admin.ModelAdmin):
    class Meta:
        model = CovidDataModel
        exclude = []


class FetchedDataFilesAdmin(admin.ModelAdmin):
    class Meta:
        model = FetchedDataFiles
        exclude = []


admin.site.register(CountryModel, CountryModelAdmin)
admin.site.register(CovidDataModel, CovidDataModelAdmin)
admin.site.register(FetchedDataFiles, FetchedDataFilesAdmin)