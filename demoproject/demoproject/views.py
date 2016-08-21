import os
from chartit import DataPool, Chart
from .models import MonthlyWeatherByCity
from .decorators import add_source_code_and_doc
from django.shortcuts import render_to_response


def homepage(_):
    ds = DataPool(
        series=[{
            'options': {
                'source': MonthlyWeatherByCity.objects.all()
            },
            'terms': [
                'month',
                'houston_temp',
                'boston_temp',
                'san_francisco_temp'
            ]
        }]
    )

    def monthname(month_num):
        names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        return names[month_num]

    cht = Chart(
        datasource=ds,
        series_options=[{
            'options': {
                'type': 'line',
                'stacking': False
            },
            'terms': {
                'month': [
                    'boston_temp',
                    'houston_temp']
            }
        }],
        chart_options={
            'title': {
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
        x_sortf_mapf_mts=(None, monthname, False))
    return render_to_response('index.html', {'chart_list': cht})


@add_source_code_and_doc
def demohome(_, title, code, doc, sidebar_items):
    """
    Welcome to the Django-Chartit Demo. This demo has a lot of sample charts
    along with the code to help you get familiarized with the Chartit API.

    The examples start with simple ones and get more and  more complicated.
    The latter examples use concepts explained in the examples earlier. So if
    the source code of a particular chart looks confusing, check to see if any
    details have already been explained in a previous example.

    The models that the examples are based on are explained in Model Details.

    Thank you and have fun exploring!
    """
    code = None
    return render_to_response('demohome.html',
                              {'chart_list': None,
                               'code': code,
                               'title': title,
                               'doc': doc,
                               'sidebar_items': sidebar_items})


@add_source_code_and_doc
def model_details(_, title, code, doc, sidebar_items):
    """
    All the charts in this section are based on the following Models.
    Model data is available as migrations, found inside charit git
    repository.
    """
    fname = os.path.join(os.path.split(os.path.abspath(__file__))[0],
                         'models.py')
    with open(fname) as f:
        code = ''.join(f.readlines())
    return render_to_response('model_details.html',
                              {'code': code,
                               'title': title,
                               'doc': doc,
                               'sidebar_items': sidebar_items})
