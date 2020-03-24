from django.urls import path

from covid.views import DailyDataList, DailyCountryList
urlpatterns = [
    path('', DailyDataList.as_view(), name="list"),
    path('<int:country_id>/', DailyCountryList.as_view(), name="list_country_state"),
]

