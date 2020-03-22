from django.http import JsonResponse

from covid.models import CountryModel, CovidDataModel


class CountryContextForTemplateMixin(object):
    def dispatch(self, request, *args, **kwargs):
        country_id = kwargs.get('country_id')
        try:
            country = CountryModel.objects.get(id=int(country_id))
        except (CountryModel.DoesNotExist, ValueError):
            return JsonResponse({"Error": "Country with COVID data doesnot exists"})
        self.country = country
        return super(CountryContextForTemplateMixin, self).dispatch(request, *args, **kwargs
                                                                    )

    def get_context_data(self, **kwargs):
        context = super(CountryContextForTemplateMixin, self).get_context_data(**kwargs)
        context['country'] = self.country
        context['country_id'] = self.country.id
        return context


class CountryStateContextForTemplateMixin(object):
    def dispatch(self, request, *args, **kwargs):
        state_name = kwargs.get('state')
        self.state = state_name
        return super(CountryStateContextForTemplateMixin, self).dispatch(request, *args, **kwargs)
