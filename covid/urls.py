from django.urls import path

from covid.views import DailyDataList, DailyCountryStateList, DailyCountryStateDataList
urlpatterns = [
    path('', DailyDataList.as_view(), name="list"),
    path('<int:country_id>/', DailyCountryStateList.as_view(), name="list_country_state"),
    path('<int:country_id>/state/<str:state>', DailyCountryStateDataList.as_view(), name="list_country_state_data")
]

