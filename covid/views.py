# Create your views here.
from django.views.generic import ListView

from covid.models import CovidDataModel, CountryModel
from lib.mixins import CountryContextForTemplateMixin


class DailyDataList(ListView):
    model = CountryModel
    queryset = CountryModel.objects.all()
    paginate_by = 10
    template_name = "listOverallCountryCases.html"

    def get_context_data(self, **kwargs):
        context = super(DailyDataList, self).get_context_data(**kwargs)
        context["global_data"] = CountryModel.get_total_data()
        context["latest_country_wise_data"] = CountryModel.get_all_latest_country_total()
        return context


class DailyCountryList(CountryContextForTemplateMixin, ListView):
    model = CovidDataModel
    queryset = CovidDataModel.objects.all()
    paginate_by = 12
    template_name = "listDailyCountryCases.html"

    def get_queryset(self):
        qs = super(DailyCountryList, self).get_queryset().filter(country=self.country).order_by('city', 'date')
        return qs
