from django.test import TestCase
from django.contrib.auth.models import User

from app_meteo.models import UserMeteoRequestHistory


class TestMeteoClass(TestCase):

    def setUp(self):
        # Установки запускаются перед каждым тестом
        user = User.objects.create_user(username="testuser", password="12345")
        UserMeteoRequestHistory.objects.create(user=user, city='Paris')


    def test_max_length_of_field_city(self):
        author = UserMeteoRequestHistory.objects.get(id=1)
        max_length = UserMeteoRequestHistory._meta.get_field('city').max_length
        self.assertEquals(max_length, 100)
