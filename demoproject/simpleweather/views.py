from django.shortcuts import render_to_response
from demoproject.utils.decorators import add_source_code_and_doc

from chartit import DataPool, Chart

from .models import MonthlyWeatherByCity, MonthlyWeatherSeattle

@add_source_code_and_doc
def basicline(request, title, code, doc, sidebar_items):
    """
    A Basic Line Chart
    ------------------
    Notice that:  

    - ``terms`` is a list of all fields (both for x-axis and y-axis) 
      to retrieve from the model.
    - ``series_options`` terms is written as ``x: [y, ...]`` pairs.
    """
    
    #start_code
    ds = DataPool(
           series=
            [{'options': {
                'source': MonthlyWeatherByCity.objects.all()},
              'terms': [
                'month',
                'houston_temp', 
                'boston_temp']}
             ])

    cht = Chart(ds, 
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
                   'text': 'Weather Data of Boston and Houston'},
               'xAxis': {
                    'title': {
                       'text': 'Month number'}}})
    #end_code
    return render_to_response('base.html', {'chart_list': cht,
                                             'code': code,
                                             'title': title,
                                             'doc': doc,
                                             'sidebar_items': sidebar_items})

@add_source_code_and_doc
def line_with_mapf_for_x(request, title, code, doc, sidebar_items):
    """
    Mapping the x-axis
    ------------------
    
    This example demonstrates how to use the ``sortf_mapf_mts`` parameter to 
    *map* the x-axis. The database only has month numbers (1-12) but not the 
    month names. To display the month names in the graph, we create the 
    ``monthname`` function and pass it to the ``Chart`` as the mapping funtion 
    (``mapf``). 
    
    Points to note: 
    
    - ``mts`` is ``False`` because we want to sort by month numbers and map to 
      the month names *after* they are sorted in order of month numbers. 
      Setting it to ``True`` would sort after mapping giving an incorrect sort 
      order like ``Apr``, ``Aug``, ``Dec``, ``...``. 
    """
    #start_code
    ds = DataPool(
           series=
            [{'options': {
                'source': MonthlyWeatherByCity.objects.all()},
              'terms': [
                'month',
                'houston_temp', 
                'boston_temp']}
             ])
    
    def monthname(month_num):
        names ={1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        return names[month_num]
    
    cht = Chart(ds, 
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
                   'text': 'Weather Data of Boston and Houston'},
               'xAxis': {
                    'title': {
                       'text': 'Month'}}},
            x_sortf_mapf_mts = (None, monthname, False))
    #end_code
    return render_to_response('base.html', {'chart_list': cht,
                                             'code': code,
                                             'title': title,
                                             'doc': doc,
                                             'sidebar_items': sidebar_items})

@add_source_code_and_doc
def line_multi_table_same_x(request, title, code, doc, sidebar_items):
    """
    Line Chart with x-axis values from multiple models
    --------------------------------------------------
    
    This example demonstrates data from two different models 
    ``MonthlyWeatherByCity`` and ``MonthlyWeatherSeattle`` on the same chart
    and on the same x-axis.
    
    Points to note:
    
    - The `month` in ``terms`` for seattle data is written as 
      ``{'month_seattle': 'month'}`` instead of as just ``'month'`` because 
      in the latter case it would overwrite the ``'month'`` term from the 
      other model.
    """
    #start_code
    ds = DataPool(
           series=
            [{'options': {
                'source': MonthlyWeatherByCity.objects.all()},
              'terms': [
                'month',
                'houston_temp', 
                'boston_temp']},
             {'options': {
                'source': MonthlyWeatherSeattle.objects.all()},
              'terms': [
                {'month_seattle': 'month'},
                'seattle_temp']}
             ])

    cht = Chart(ds, 
            series_options = 
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'month': [
                    'boston_temp',
                    'houston_temp'],
                  'month_seattle': [
                    'seattle_temp']
                  }}],
            chart_options = 
              {'title': {
                   'text': 'Weather from 2 different tables'},
               'xAxis': {
                    'title': {
                       'text': 'Month number'}}})
    #end_code
    return render_to_response('base.html', {'chart_list': cht,
                                             'code': code,
                                             'title': title,
                                             'doc': doc,
                                             'sidebar_items': sidebar_items})

