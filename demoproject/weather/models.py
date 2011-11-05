from django.db import models

# Create your models here.

class City(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    city = models.CharField(max_length=50, db_column='city')
    state = models.CharField(max_length=2, db_column='state')
    
    def __unicode__(self):
        return '%s, %s' %(self.city, self.state)
    def region(self):
        return 'USA'
    
    class Meta:
        db_table = 'city'
        

class DailyWeather(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    month = models.IntegerField(db_column='month')
    day = models.IntegerField(db_column='day')
    temperature = models.DecimalField(max_digits=5, decimal_places=1,
                                      db_column='temperature')
    city = models.CharField(max_length=50, db_column='city')
    state = models.CharField(max_length=2, db_column='state')
    
    class Meta:
        db_table = 'daily_weather'