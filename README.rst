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

* master
    * Update demo with an example of how to pass ``legendIndex`` as an option
      to a data serie. Closes
      `#48 <https://github.com/chartit/django-chartit/issues/48>`_.
    * Update demo with an example of how to change the label of any term
      instead of using the default one. Closes
      `#46 <https://github.com/chartit/django-chartit/issues/46>`_.

* 0.2.9 (January 17, 2017)
    * Enable pylint during testing but don't block Travis-CI on failures. Closes
      `#42 <https://github.com/chartit/django-chartit/issues/42>`_.
    * Handle unicode data in pie and scatter plot charts under Python 2.7.
      `PR#47 <https://github.com/chartit/django-chartit/pull/47>`_.


* 0.2.8 (December 4, 2016)
    * ``PivotChart`` and ``PivotDataPool`` **will be deprecated soon**. Both
      are marked with deprecation warnings. There is a lot of duplication and
      special handling between those classes and the ``Chart`` and ``DataPool``
      classes which make it harder to expand the feature set for django-chartit.
      The next release will focus on consolidating all the functionality into
      ``Chart`` and ``DataPool`` so that users will still be able to draw pivot
      charts. You will have to construct your pivot charts manually though!
    * ``DataPool`` terms now supports model properties. Fixes
      `#35 <https://github.com/chartit/django-chartit/issues/35>`_.
      Model properties are **not** supported for ``PivotDataPool``!
      **WARNING: when using model properties chartit can't make use of
      ``QuerySet.values()`` internally. This means results will not be groupped
      by the values of the fields you supplied. This may lead to unexpected
      query results/charts!**
    * ``DataPool`` now supports ``RawQuerySet`` as data source. Fixes
      `#44 <https://github.com/chartit/django-chartit/issues/44>`_.
      ``RawQuerySet`` is **not** supported for ``PivotDataPool``!
      **WARNING: when using ``RawQuerySet`` don't use double underscores
      in field names because these are interpreted internally by chartit and
      will cause exceptions. For example don't do this
      ``SELECT AVG(rating) as rating__avg`` instead write it as
      ``SELECT AVG(rating) as rating_avg``!**
    * README now tells how to execute ``demoproject/``

* 0.2.7 (September 14, 2016)
    * Don't use ``super(self.__class__)`` b/c that breaks chart class
      inheritance.
      Fixes `#41 <https://github.com/chartit/django-chartit/issues/41>`_

* 0.2.6 (August 16, 2016)
    * Merge ``chartit_tests/`` with ``demoproject/``
    * Load test DB with real data to use during testing
    * Add more tests
    * Update the path to demoproject.settings when building docs. Fixes
      a problem which caused some API docs to be empty
    * Fix ValueError: not enough values to unpack (expected 2, got 0)
      with PivotChart when the QuerySet returns empty data
    * Dropped requirement on ``simplejson``
    * Properly handle unicode data in Pivot charts. Fixes
      `#5 <https://github.com/chartit/django-chartit/issues/5>`_
    * Demo project updated with Chart and PivotChart examples of
      rendering DateField values on the X axis
    * Allow charting of ``extra()`` or ``annotate()`` fields. Fixes
      `#8 <https://github.com/chartit/django-chartit/issues/8>`_ and
      `#12 <https://github.com/chartit/django-chartit/issues/12>`_
    * Refactor ``RecursiveDefaultDict`` to allow chart objects to be
      serialized to/from cache. Fixes
      `#10 <https://github.com/chartit/django-chartit/issues/10>`_
    * Add information about supported 3rd party JavaScript versions. Fixes
      `#14 <https://github.com/chartit/django-chartit/issues/14>`_

* 0.2.5 (August 3, 2016)
    * Workaround Python 3 vs. Python 2 list sort issue which breaks
      charts with multiple data sources displayed on the same axis!
    * Make demoproject/ compatible with Django 1.10

* 0.2.4 (August 2, 2016)
    * Fix for ``get_all_field_names()`` and ``get_field_by_name()`` removal
      in Django 1.10. Fixes
      `#39 <https://github.com/chartit/django-chartit/issues/39>`_
    * Updated for django.db.sql.query.Query.aggregates removal

* 0.2.3 (July 30, 2016)
    * New to_json() method for charts. Useful for creating Highcharts in AJAX
    * Merged with *django-chartit2* fork by
      `Grant McConnaughey <https://github.com/grantmcconnaughey>`_ which adds
      Python 3 and latest Django 1.8.x and 1.9.x support
    * Allow dictionary fields in conjunction with lambda fields. Closes
      `#26 <https://github.com/chartit/django-chartit/issues/26>`_
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
out the ``demoproject/`` directory. To execute the demo run the commands ::

    cd demoproject/
    PYTHONPATH=../ python ./manage.py migrate
    PYTHONPATH=../ python ./manage.py runserver

===============
Documentation
===============

Full documentation is available
`here <http://django-chartit.readthedocs.org/en/latest/?badge=latest>`_ .

=============================
Required JavaScript Libraries
=============================

The following JavaScript Libraries are required for using Django-Chartit.

- `jQuery <http://jquery.com>`_ - versions 1.6.4 and 1.7 are known
  to work well with django-chartit.
- `Highcharts <http://highcharts.com>`_ - versions 2.1.7 and 2.2.0 are known
  to work well with django-chartit.

.. note:: While ``Django-Chartit`` itself is licensed under the BSD license,
   ``Highcharts`` is licensed under the `Highcharts license
   <http://www.highcharts.com/license>`_ and ``jQuery`` is licensed under both
   MIT License and GNU General Public License (GPL) Version 2. It is your own
   responsibility to abide by respective licenses when downloading and using
   the supporting JavaScript libraries.
