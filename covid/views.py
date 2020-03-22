from django.db.models import Count, Sum, Max
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView, DetailView

from covid.models import CovidDataModel, CountryModel
from lib.mixins import CountryContextForTemplateMixin, CountryStateContextForTemplateMixin


class DailyDataList(ListView):
    model = CountryModel
    queryset = CountryModel.objects.order_by('-country')
    paginate_by = 20
    template_name = "list_countries.html"

    def get_context_data(self, **kwargs):
        context = super(DailyDataList, self).get_context_data(**kwargs)
        context['countries_data'] = CountryModel.objects.values('country').annotate(affected_states=Count('coviddatamodel__state',
                                                                                               distinct=True),
                                                                          total_deaths=Max('coviddatamodel__deaths'),
                                                                          confirmed_cases=Max(
                                                                              'coviddatamodel__confirmed_cases'),
                                                                          recovered=Max(
                                                                              'coviddatamodel__recovered'),
                                                                          last_updated=Max('coviddatamodel__date'))\
            .values('country', 'affected_states', 'total_deaths', 'confirmed_cases', 'recovered', 'id', 'last_updated')\
            .order_by('-total_deaths')
        return context


class DailyCountryStateList(CountryContextForTemplateMixin, ListView):
    model = CovidDataModel
    queryset = CovidDataModel.objects.all()
    paginate_by = 12
    template_name = "list_country_state_view.html"

    def get_queryset(self):
        qs = super(DailyCountryStateList, self).get_queryset().filter(country=self.country).order_by('state', 'date')
        return qs


class DailyCountryStateDataList(CountryContextForTemplateMixin, CountryStateContextForTemplateMixin, ListView):
    model = CovidDataModel
    queryset = CovidDataModel.objects.all()
    paginate_by = 12
    template_name = "list_country_state_data_view.html"

    def get_queryset(self):
        qs = super(DailyCountryStateDataList, self).get_queryset().filter(country=self.country, state=self.state) \
            .order_by('date')
        return qs
