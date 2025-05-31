# pylint: disable=C0103
""" Настройки URL приложения cart """

from django.urls import path

from app_meteo.views import MeteoView


urlpatterns = [
    path("", MeteoView.as_view(), name="meteo"),
]