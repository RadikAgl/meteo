from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from app_meteo.forms import CityForm
from app_meteo.weather import get_weather


class MeteoView(View):
    form_class = CityForm

    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        meteo_data = "Empty"
        if form.is_valid():
            form_data = form.cleaned_data
            city = form_data["city_name"]
            meteo_data = get_weather(city)

        return render(request, self.template_name, {"form": form, "meteo_data": meteo_data})