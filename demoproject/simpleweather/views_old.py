import inspect
from django.shortcuts import render_to_response
from chartit import DataPool, Chart
from .models import MonthlyWeatherByCity, MonthlyWeatherSeattle


import os
import textwrap
from django import template
from django.conf import settings
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe

def rstfy(value):
    try:
        from docutils.core import publish_parts
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Cannot rstfy. The Python " 
            "docutils library isn't installed.")
        return force_unicode(value)
    else:
        parts = publish_parts(source=smart_str(value), writer_name="html4css1")
        return mark_safe(force_unicode(parts["title"])), mark_safe(force_unicode(parts["fragment"]))

def get_docstring_and_code(func):
    doc = textwrap.dedent(eval(func).__doc__)
    doc_title, doc_body = rstfy(doc)
    
    with open(os.path.abspath( __file__ )) as f:
        all_code = f.readlines()
        for i, line in enumerate(all_code):
            if 'def ' in line and func in line:
                func_start = i
                break
            
        for i, line in enumerate(all_code[func_start:]):
            if '#start_code' in line:
                code_start = func_start+i+1
                break
        
        for i, line in enumerate(all_code[code_start:]):
            if '#end_code' in line:
                code_end = code_start+i
                break
        
        indent = None
        clean_code = []
        after_whitespace = False
        code = all_code[code_start:code_end]
        
        for line in code[:]:
            if not after_whitespace:
                if not line.strip():
                    pass
                else:
                    indent = len(line) - len(line.strip()) - 1
                    clean_code.append(line[indent:])
                    after_whitespace = True
            else:
                if not line.strip():
                    clean_code.append(line)
                else:
                    clean_code.append(line[indent:])
        
    return (''.join(clean_code), doc_title, doc_body)






def get_video(request, func):
    video = {}
    return render_to_response('video.html', {'video': video.get(func)})



def basicline(request):
    """
    A Basic Line Chart
    ==================
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
    frame = inspect.currentframe()
    func_name = inspect.getframeinfo(frame)[2]
    source_code, doc_title, doc_body = get_docstring_and_code(func_name)
    return render_to_response('base2.html', {'chart_list': cht,
                                             'source_code': source_code,
                                             'doc_title': doc_title,
                                             'doc_body': doc_body})

def line_with_mapf_for_x(request):
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
    return render_to_response('base2.html', {'chart_list': cht})

def line_multi_table_same_x(request):
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
    return render_to_response('base2.html', {'chart_list': cht})