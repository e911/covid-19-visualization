from django.urls import path

from covid.views import DailyDataList, DailyCountryList, NewDailyDataList

urlpatterns = [
    path('', DailyDataList.as_view(), name="list"),
    path('new_ui_ongoing', NewDailyDataList.as_view(), name="new_list"),
    path('<int:country_id>/', DailyCountryList.as_view(), name="list_country_state"),
]

