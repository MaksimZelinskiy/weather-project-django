# pip install beautifulsoup4
# pip install requests
# pip install lxml
# pip install selenium
# pip install schedule
# pip install celery
# pip install redis
# python -m celery -A django_celery worker


import schedule
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver

from config import path


def parse_weather_info():
    print("start parse")

    # открытие веб браузера
    dr = webdriver.Chrome()
    # открытия страницы
    dr.get("https://pogoda.meta.ua/Kyivska/Kyivskiy/Kyiv/5/")

    # обработка страницы по HTML
    bs = BeautifulSoup(dr.page_source, "lxml")

    # поиск нужных div`ов (для безопасности)
    all_5days = bs.find('div', class_='five-days__desktop-wrap')
    # list: [] поиск результатов погоды (5 дней)
    list_days_descript_result = all_5days.find_all('div', class_='five-days__day fl-col')

    # Переменные для цикла и сохранение результата
    date, results = datetime.now(), {}

    # старт цикла получение результатов о погоде
    date_var_description = date
    for day_result in list_days_descript_result:
        # изменение формата времени для ключа
        date_cycle = date_var_description.strftime("%d.%m.%Y %H")

        # получение нужного div`а для описания (в нем есть результат погоды)
        icons = day_result.find('div', class_='five-days__icon')
        # получение div`а для температуры
        temperature_div = day_result.find('div', class_="five-days__temp fl-col")

        # запись в dict результата по погоде (ключ является датой)
        results[str(date_cycle)] = {
            "description": icons["data-tippy-content"],
            "temperature": {
                "high": temperature_div.find('span', class_="high").get_text(),
                "low": temperature_div.find('span', class_="low").get_text()
                }
            }

        # +1 шаг цикла == +1 день к дате
        date_var_description = date_var_description + timedelta(days=1)


    return results


def parse_weather_every_day():

    import json
    with open(f"{path}/parameters/parse.json") as json_parameters:
        parameters_parse = json.load(json_parameters)

    time_parse = parameters_parse["time"]
    schedule.every().day.at(f"{time_parse}:59").do(parse_weather_info)


    while True:
        schedule.run_pending()
        time.sleep(50)
