from django import forms


class CityForm(forms.Form):
    city_name = forms.CharField(label="City name", max_length=100)
