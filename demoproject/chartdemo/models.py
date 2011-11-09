from django.db import models


class MonthlyWeatherByCity(models.Model):
    month = models.IntegerField()
    boston_temp = models.DecimalField(max_digits=5, decimal_places=1)
    houston_temp = models.DecimalField(max_digits=5, decimal_places=1)
    new_york_temp = models.DecimalField(max_digits=5, decimal_places=1)
    san_franciso_temp = models.DecimalField(max_digits=5, decimal_places=1)
    
class MonthlyWeatherSeattle(models.Model):
    month = models.IntegerField()
    seattle_temp = models.DecimalField(max_digits=5, decimal_places=1)
    
class DailyWeather(models.Model):
    month = models.IntegerField()
    day = models.IntegerField()
    temperature = models.DecimalField(max_digits=5, decimal_places=1)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)