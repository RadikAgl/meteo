from django.test import TestCase

from app_meteo.weather import get_time


class WeatherFunctionsTest(TestCase):
    """Класс для тестирования функций для получения прогноза погоды"""

    def test_get_time(self) -> None:
        """Тест функции извлечения времени из временной метки"""

        timestamp = 1748851400
        hour_minute = get_time(timestamp)
        self.assertEqual(hour_minute, "08:03")

    def test_