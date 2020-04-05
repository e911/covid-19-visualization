# Create your views here.
from django.http import JsonResponse
from django.views.generic import ListView

from covid.models import CovidDataModel, CountryModel
from lib.mixins import CountryContextForTemplateMixin


class DailyDataList(ListView):
    model = CountryModel
    queryset = CountryModel.get_all_latest_country_total()
    paginate_by = 10
    template_name = "listOverallCountryCases.html"

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            super(DailyDataList, self).get(request, *args, **kwargs)
            get_cases_data, get_deaths_data, get_recovered_data = CountryModel.get_bar_graph_data()
            return JsonResponse({"cases": get_cases_data, "deaths": get_deaths_data, "recovered": get_recovered_data})
        return super(DailyDataList, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DailyDataList, self).get_context_data(**kwargs)
        context["global_data"] = CountryModel.get_total_data()
        return context


class DailyCountryList(CountryContextForTemplateMixin, ListView):
    model = CovidDataModel
    queryset = CovidDataModel.objects.all()
    paginate_by = 12
    template_name = "listDailyCountryCases.html"

    def get_queryset(self):
        qs = super(DailyCountryList, self).get_queryset().filter(country=self.country).order_by('city', 'date')
        return qs
