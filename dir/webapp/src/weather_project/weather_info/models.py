from django.db import models


class Weather_info(models.Model):
    date = models.TextField()
    weather_description = models.TextField()
    temperature = models.TextField()

    def __str__(self):
        return self.date