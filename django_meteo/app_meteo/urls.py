from django.urls import path

from app_meteo.views import MeteoView, MeteoHistoryApi

urlpatterns = [
    path("", MeteoView.as_view(), name="meteo"),
    path("api/", MeteoHistoryApi.as_view(), name="api_meteohistory"),
]
