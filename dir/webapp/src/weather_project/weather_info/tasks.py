import requests as r
import uuid
from celery import shared_task
from django.conf import settings

from .parse import parse_weather_info

@shared_task
def parse_weather():
    parse_weather_info()