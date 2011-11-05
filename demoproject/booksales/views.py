from django.shortcuts import render_to_response
from django.db.models import Sum, Avg

from chartit import PivotChart, PivotDataPool

from .models import SalesHistory

def saleschart(request):
    ds = PivotDataPool(
            [{'options':{
                'source': SalesHistory.objects.all(),
                'categories': [
                  'bookstore__city__state', 
                  'bookstore__city__city'],
                'legend_by': [
                  'book__genre__name'],
                'top_n_per_cat': 2},
              'terms': {
                'tot_price': Sum('price'),
                'avg_sales': {
                  'func':Avg('sale_qty'),
                  'legend_by':()}}}],
            top_n = 5,
            pareto_term = 'avg_sales',
            top_n_term = 'avg_sales')
    
    pc1 = PivotChart(
            datasource = ds, 
            series_options = [{'options': {'type': 'column',
                                         'stacking': True, 
                                         'xAxis': 0,
                                         'yAxis': 0},
                             'terms': ['tot_price', 
                                       {'avg_sales': {'type': 'line',
                                                      'yAxis': 1,
                                                      'zIndex': 2}}]}],
            chart_options = {'chart': {'renderTo': 'container1',
                                       'zoomType': 'y'},
                             'credits': {'enabled': False},
                             'yAxis': [{}, {'opposite': True}]})
    pc2 = PivotChart(datasource = ds,
            series_options = [{'options': {'type': 'column',
                                         'stacking': True, 
                                         'xAxis': 0,
                                         'yAxis': 0},
                             'terms': ['avg_sales']}],
            chart_options = {'chart': {'renderTo': 'container2'},
                             'credits': {'enabled': False}})
    
    return render_to_response('booksales/pivotcharts.html', 
                              {'salescharts': [pc1, pc2]})
    