from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta

from .models import Weather_info
from .parse import parse_weather_info
from .serializers import Weather_serializer

# Функция получения данных о погоде (за все время)
class WeatherAPIView(APIView):
    def get(self, request):
        # поиск данных
        lst = Weather_info.objects.all().values()
        # возвращение результата поиска (данных)
        return Response({'all_days': list(lst)})

# Функция получения данных о погоде (за сегодня)
class WeatherAPIViewNow(APIView):
    def get(self, request):
        # Получение ключа для поиска
        date_now = datetime.now().strftime("%d.%m.%Y %H")
        # Поиск данных по фильтру (ключ is дата)
        queryset = Weather_info.objects.filter(date=date_now).values()
        # возвращение результата поиска (данных)
        return Response({date_now: queryset})

# Функция запуск таска (парсинг по post запрос)
class WeatherAPIParse(APIView):

    # в этой функции есть post запрос для старта парсинга
    def post(self, request):
        # Парсим данные и сохраняем в переменную
        dict_result = parse_weather_info()

        # Цикл по результатам данных по погоде
        for date in dict_result:
            # сохранение данных в переменные
            date_var, description_var, temperature_var = date, dict_result[date]["description"], dict_result[date]["temperature"]["high"] + "/" + dict_result[date]["temperature"]["low"]

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
                Weather_info.objects.filter(date=date_var).update(weather_description=description_var, temperature=temperature_var)

        return Response({'result': 'successfully completed'})


# класс для изменения времени парсинга (парсинг по post запрос)
class WeatherAPIParseNewTime(APIView):

    def post(self, request, *args, **kwargs):
        new_time = kwargs.get("time", None)

        import json
        from config import path
        with open(f"{path}/parameters/parse.json") as json_file:
            parse_json = json.load(json_file)

        parse_json["time"] = new_time

        with open(f"{path}/parameters/parse.json", "w") as json_file:
            json.dump(parse_json, json_file)

        return Response({'result': 'successfully completed'})
