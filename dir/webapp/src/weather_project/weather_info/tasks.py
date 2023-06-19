import requests as r
import uuid
from celery import shared_task
from django.conf import settings
from .models import Weather_info

from .parse import parse_weather_info

@shared_task
def parse_weather():
    dict_result = parse_weather_info()

    # Цикл по результатам данных по погоде
    for date in dict_result:

        date_var, description_var, temperature_var = date, dict_result[date]["description"], \
                                                     dict_result[date]["temperature"]["high"] + "/" + \
                                                     dict_result[date]["temperature"]["low"]

        # Проверка есть ли в БД данный день
        if list(Weather_info.objects.filter(date=date_var).values()) == []:
            # Если нет, то создаем
            Weather_info.objects.create(
                date=date_var,
                weather_description=description_var,
                temperature=temperature_var
            )
        else:
            # Если уже есть, то обновляем данные
            Weather_info.objects.filter(date=date_var).update(weather_description=description_var,
                                                          temperature=temperature_var)
