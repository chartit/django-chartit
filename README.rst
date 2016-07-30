################
Django-Chartit
################

.. image:: https://readthedocs.org/projects/django-chartit/badge/?version=latest
    :target: http://django-chartit.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/chartit/django-chartit.svg?branch=master
    :target: https://travis-ci.org/chartit/django-chartit

.. image:: https://landscape.io/github/chartit/django-chartit/master/landscape.svg?style=flat
   :target: https://landscape.io/github/chartit/django-chartit/master
   :alt: Code Health

.. image:: https://coveralls.io/repos/github/chartit/django-chartit/badge.svg?branch=master
  :target: https://coveralls.io/github/chartit/django-chartit?branch=master


Django Chartit is a Django app that can be used to easily create charts from the data
in your database. The charts are rendered using ``Highcharts`` and ``jQuery``
JavaScript libraries. Data in your database can be plotted as simple line
charts, column charts, area charts, scatter plots, and many more chart types.
Data can also be plotted as Pivot Charts where the data is grouped and/or
pivoted by specific column(s).

=========
Changelog
=========

* 0.2.3 (July 30, 2016)
    * New to_json() method for charts. Useful for creating Highcharts in AJAX
    * Merged with *django-chartit2* fork by
      `Grant McConnaughey <https://github.com/grantmcconnaughey>`_ which adds
      Python 3 and latest Django 1.8.x and 1.9.x support
    * Allow dictionary fields in conjunction with lambda fields. Closes #26
    * Documentation improvements
    * Lots of code cleanups and style improvements

* 0.2.2 as django-chartit2 (January 28, 2016)
    * Fixed another issue that prevented installation via PyPI

* 0.2.0 as django-chartit2 (January 20, 2016):
    * Fixed issue that could prevent installation via PyPI

* 0.1 (November 5, 2011)
    * Initial release of django-chartit

========
Features
========

- Plot charts from models.
- Plot data from multiple models on the same axis on a chart.
- Plot pivot charts from models. Data can be pivoted by across multiple
  columns.
- Legend pivot charts by multiple columns.
- Combine data from multiple models to plot on same pivot charts.
- Plot a pareto chart, paretoed by a specific column.
- Plot only a top few items per category in a pivot chart.
- Python 3 compatibility
- Django 1.8 and 1.9 compatibility
- Documentation to ReadTheDocs
- Automated testing via Travis CI
- Test coverage tracking via Coveralls

============
Installation
============

You can install Django-Chartit from PyPI. Just do ::

    $ pip install django_chartit

Then, add `chartit` to `INSTALLED_APPS` in "settings.py".

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
and Houston. ::

   class MonthlyWeatherByCity(models.Model):
       month = models.IntegerField()
       boston_temp = models.DecimalField(max_digits=5, decimal_places=1)
       houston_temp = models.DecimalField(max_digits=5, decimal_places=1)

And let's say we want to create a simple line chart of month on the x-axis
and the temperatures of the two cities on the y-axis. ::

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
following model. ::

   class DailyWeather(models.Model):
       month = models.IntegerField()
       day = models.IntegerField()
       temperature = models.DecimalField(max_digits=5, decimal_places=1)
       rainfall = models.DecimalField(max_digits=5, decimal_places=1)
       city = models.CharField(max_length=50)
       state = models.CharField(max_length=2)

We want to plot a pivot chart of month (along the x-axis) versus the average
rainfall (along the y-axis) of the top 3 cities with highest average
rainfall in each month. ::

    from django.db.models import Avg
    from chartit import PivotDataPool, PivotChart

    def rainfall_pivot_chart_view(request):
        # Step 1: Create a PivotDataPool with the data we want to retrieve.
        rainpivotdata = PivotDataPool(
            series=[{
                'options': {
                    'source': DailyWeather.objects.all(),
                    'categories': ['month'],
                    'legend_by': 'city',
                    'top_n_per_cat': 3,
                },
                'terms': {
                    'avg_rain': Avg('rainfall'),
                }
            }]
        )

        # Step 2: Create the PivotChart object
        rainpivcht = PivotChart(
            datasource=rainpivotdata,
            series_options=[{
                'options': {
                    'type': 'column',
                    'stacking': True
                },
                'terms': ['avg_rain']
            }],
            chart_options={
                'title': {
                    'text': 'Rain by Month in top 3 cities'
                },
                'xAxis': {
                    'title': {
                        'text': 'Month'
                    }
                }
            }
        )

        # Step 3: Send the PivotChart object to the template.
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

=========================
Rendering multiple charts
=========================

It is possible to render multiple charts in the same template. The first
argument to ``load_charts`` is the Chart object or a list of Chart objects,
and the second is a comma separated list of HTML IDs where the charts will
be rendered.

When calling Django's ``render`` you have to pass all you charts as a list::

    return render(request, 'index.html',
                 {
                    'chart_list' : [chart_1, chart_2],
                 }
            )

Then in your template you have to use the proper syntax::

    <head>
        {% load chartit %}
        {{ chart_list|load_charts:"chart_1,chart_2" }}
    </head>
    <body>
        <div id="chart_1">First chart will be rendered here</div>
        <div id="chart_2">Second chart will be rendered here</div>
    </body>

====
Demo
====

The above examples are just a brief taste of what you can do with
Django-Chartit. For more examples and to look at the charts in actions, check
out the `demo website <http://chartit.shutupandship.com/demo>`_.

===============
Documentation
===============

Full documentation is available
`here <http://django-chartit.readthedocs.org/en/latest/?badge=latest>`_ .

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
