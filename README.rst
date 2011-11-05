
###############
Django-Chartit 
###############

Django-Chartit can be used to plot the data from various models in your Django 
project directly onto the web pages. The charts are rendered using the 
``Highcharts`` and ``jQuery`` JavaScript libraries. Data in your database can 
be plotted as simple line charts, column charts, area charts, scatter plots, and 
many more chart types. Data can also be plotted as Pivot Charts where the data 
is grouped and/or pivoted by specific column(s).

========
Features
========

- Plot charts from models.
- Plot data from multiple models on the same axis on a chart.
- Plot pivot charts from models. Data can be pivoted by multiple columns.
- Legend pivot charts by multiple columns.
- Combine data from multiple models to plot on same pivot charts.
- Plot a pareto chart, paretoed by a specific column.
- Plot only a top few items per category in a pivot chart.

============
Installation
============

You can install Django-Chartit from PyPI. Just do ::

    $ pip install django_chartit

You also need supporting JavaScript libraries. See the 
`Required JavaScript Libraries`_ section for more details. 

==========
How to Use
==========

Plotting a chart or pivot chart on a webpage involves the following steps.

1. Create a ``DataPool`` or ``PivotDataPool`` object that specifies what data 
   you need to retrieve and from where. 
2. Create a ``Chart`` or ``PivotChart`` object to plot the data in the 
   ``DataPool`` or ``PivotDataPool`` respectively.
3. Return the ``Chart``/``PivotChart`` object from a django ``view`` function 
   to the django template.
4. Use the ``load_charts`` template tag to load the charts to HTML tags with 
   specific `ids`.

It is easier to explain the steps above with examples. So read on.

====================
How to Create Charts
====================
Here is a short example of how to create a line chart. Let's say we have a 
simple model with 3 fields - one for month and two for temperatures of Boston 
and Houston.

.. code-block:: python
   :linenos:
   
   class MonthlyWeatherByCity(models.Model):
       month = models.IntegerField()
       boston_temp = models.DecimalField(max_digits=5, decimal_places=1)
       houston_temp = models.DecimalField(max_digits=5, decimal_places=1)

And let's say we want to create a simple line chart of month on the x-axis 
and the temperatures of the two cities on the y-axis. 

.. code-block:: python
   :linenos:
   
   from chartit import DataPool, Chart
   
   def weather_chart_view(request):
       #Step 1: Create a DataPool with the data we want to retrieve.
       weatherdata = \
           DataPool(
              series=
               [{'options': {
                  'source': MonthlyWeatherByCity.objects.all()},
                 'terms': [
                   'month',
                   'houston_temp', 
                   'boston_temp']}
                ])
       
       #Step 2: Create the Chart object
       cht = Chart(
               datasource = weatherdata, 
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
       
       #Step 3: Send the chart object to the template.
       return render_to_response({'weatherchart': cht})

And you can use the ``load_charts`` filter in the django template to render 
the chart. ::

  <head> 
      <!-- code to include the highcharts and jQuery libraries goes here -->
      <!-- load_charts filter takes a comma-separated list of id's where -->
      <!-- the charts need to be rendered to                             -->
      {% load chartit %}
      {{ weatherchart|load_charts:"container" }}
  </head>
  <body>
      <div id='container'> Chart will be rendered here </div>
  </body>

===========================
How to Create Pivot Charts
===========================

Here is an example of how to create a pivot chart. Let's say we have the 
following model. 

.. code-block:: python
   :linenos:

   class DailyWeather(models.Model):
       month = models.IntegerField()
       day = models.IntegerField()
       temperature = models.DecimalField(max_digits=5, decimal_places=1)
       rainfall = models.DecimalField(max_digits=5, decimal_places=1)
       city = models.CharField(max_length=50)
       state = models.CharField(max_length=2)

We want to plot a pivot chart of month (along the x-axis) versus the average 
rainfall (along the y-axis) of the top 3 cities with highest average 
rainfall in each month.

.. code-block:: python
   :linenos:
   
   from chartit import PivotDataPool, PivotChart
   
   def rainfall_pivot_chart_view(request):
       #Step 1: Create a PivotDataPool with the data we want to retrieve.
       rainpivotdata = \
           PivotDataPool(
              series =
               [{'options': {
                  'source': DailyWeather.objects.all(),
                  'categories': ['month']},
                 'terms': {
                   'avg_rain': Avg('rainfall'),
                   'legend_by': ['city'],
                   'top_n_per_cat': 3}}
                ])
       
       #Step 2: Create the PivotChart object
       rainpivcht = \
           PivotChart(
               datasource = rainpivotdata, 
               series_options = 
                 [{'options':{
                     'type': 'column',
                     'stacking': True},
                   'terms':[
                     'avg_rain']}],
               chart_options = 
                 {'title': {
                      'text': 'Rain by Month in top 3 cities'},
                  'xAxis': {
                       'title': {
                          'text': 'Month'}}})
       
       #Step 3: Send the PivotChart object to the template.
       return render_to_response({'rainpivchart': rainpivcht})

And you can use the ``load_charts`` filter in the django template to render 
the chart. ::

  <head> 
      <!-- code to include the highcharts and jQuery libraries goes here -->
      <!-- load_charts filter takes a comma-separated list of id's where -->
      <!-- the charts need to be rendered to                             -->
      {% load chartit %}
      {{ rainpivchart|load_charts:"container" }}
  </head>
  <body>
      <div id='container'> Chart will be rendered here </div>
  </body>

====
Demo
====

The above examples are just a brief taste of what you can do with 
Django-Chartit. For more examples and to look at the charts in actions, see 
the demo website.

===============
API Reference
===============
.. toctree::
   :maxdepth: 3
   
   apireference

=============================
Required JavaScript Libraries
=============================

The following JavaScript Libraries are required for using Django-Chartit.

- `jQuery <http://jquery.com>`_
- `Highcharts <http://highcharts.com>`_

.. note:: While ``Django-Chartit`` itself is licensed under the BSD license, 
   ``Highcharts`` is licensed under the `Highcharts license 
   <http://www.highcharts.com/license>`_ and ``jQuery`` is licensed under both 
   MIT License and GNU General Public License (GPL) Version 2. It is your own
   responsibility to abide by respective licenses when downloading and using 
   the supporting JavaScript libraries.

