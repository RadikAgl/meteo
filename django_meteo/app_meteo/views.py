from django.shortcuts import render
from django.views.generic import View

from app_meteo.forms import CityForm
from app_meteo.models import UserMeteoRequestHistory
from app_meteo.weather import get_weather


class MeteoView(View):
    form_class = CityForm

    template_name = "app_meteo/index.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}
        if request.user.is_authenticated:
            last_city = UserMeteoRequestHistory.objects.filter(
                user=request.user
            ).first()
            context["last_city"] = last_city
        last_city_param = request.GET.get("last_city", "")
        if last_city_param:
            context["meteo_data"] = get_weather(last_city_param)

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            city = form_data["city_name"]
            meteo_data = get_weather(city)
            if request.user.is_authenticated:
                UserMeteoRequestHistory.objects.create(user=request.user, city=city)

        return render(
            request, self.template_name, {"form": form, "meteo_data": meteo_data}
        )
