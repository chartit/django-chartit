from django.shortcuts import render_to_response
from demoproject.chartdemo.models import MonthlyWeatherByCity
from chartit import DataPool, Chart

def homepage(request):
    ds = DataPool(
       series=
        [{'options': {
            'source': MonthlyWeatherByCity.objects.all()},
          'terms': [
            'month',
            'houston_temp', 
            'boston_temp',
            'san_franciso_temp']}
         ])
    def monthname(month_num):
        names ={1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        return names[month_num]
    cht = Chart(
        datasource = ds, 
        series_options = 
          [{'options':{
              'type': 'line',
              'stacking': False},
            'terms':{
              'month': [
                'boston_temp',
                'houston_temp']
              }}],
        chart_options = 
          {'title': {
               'text': 'Weather by Month'},
           'xAxis': {
                'title': {
                   'text': 'Month'}},
           'yAxis': {
                'title': {
                    'text': 'Temperature'}},
           'legend': {
                'enabled': False},
           'credits': {
                'enabled': False}},
         x_sortf_mapf_mts = (None, monthname, False))
    return render_to_response('index.html', {'chart_list': cht})