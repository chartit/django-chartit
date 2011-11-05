from django.db import models


class MonthlyWeatherByCity(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    month = models.IntegerField()
    boston_temp = models.DecimalField(max_digits=5, decimal_places=1, 
                                      db_column='boston_temp')
    houston_temp = models.DecimalField(max_digits=5, decimal_places=1, 
                                       db_column='houston_temp')
    new_york_temp = models.DecimalField(max_digits=5, decimal_places=1, 
                                        db_column='new_york_temp')
    san_franciso_temp = models.DecimalField(max_digits=5, decimal_places=1, 
                                            db_column='san_franciso_temp')
    
    class Meta:
        db_table = 'monthly_weather_by_city'
    
class MonthlyWeatherSeattle(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    month = models.IntegerField()
    seattle_temp = models.DecimalField(max_digits=5, decimal_places=1,
                                       db_column='seattle_temp')
    
    class Meta:
        db_table = 'monthly_weather_seattle'