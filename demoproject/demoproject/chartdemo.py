from chartit import DataPool, Chart
from django.db.models import Avg, Count
from django.shortcuts import render_to_response
from .decorators import add_source_code_and_doc
from .models import MonthlyWeatherByCity, MonthlyWeatherSeattle, DailyWeather
from .models import SalesHistory, BookStore, Book


@add_source_code_and_doc
def basicline(_, title, code, doc, sidebar_items):
    """
    A Basic Line Chart
    ------------------
    This is just a simple line chart with data from 2 different columns.

    Points to note:

    - ``terms`` is a list of all fields (both for x-axis and y-axis)
      to retrieve from the model.
    - Remember that for a Chart, the x and y terms in the ``series_options``
      are written as ``x: [y, ...]`` pairs.
    - Any valid items in the `Highcharts options object
      <http://api.highcharts.com/highcharts>`_ are valid ``chart_options``.
    """

    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': MonthlyWeatherByCity.objects.all()
                },
                'terms': [
                    'month',
                    'houston_temp',
                    'boston_temp'
                ]
            }]
    )

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
                        'houston_temp'
                    ]
                }
            }],
            chart_options={
                'title': {
                    'text': 'Weather Data of Boston and Houston'
                },
                'xAxis': {
                    'title': {
                        'text': 'Month number'
                    }
                }
            }
    )
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': cht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def basicpie(_, title, code, doc, sidebar_items):
    """
    A Basic Pie Chart
    ------------------
    This is a pie chart of temperature by month for Boston.

    Points to note:

    - ``terms`` is a list of all fields (both for x-axis and y-axis)
      to retrieve from the model.
    - Remember that for a Chart, the x and y terms in the ``series_options``
      are written as ``x: [y, ...]`` pairs.
    - Any valid items in the `Highcharts options object
      <http://api.highcharts.com/highcharts>`_ are valid ``chart_options``.
    - We use the ``x_mapf_sortf_mts`` parameter to convert the month numbers
      retrieved from the database to month names.

    Note: This demo is to demonstrate the use of the API and not to teach
    you data analysis and data presentation skills. Not all charts plotted
    in this demo may make sense in real life applications. But they can
    still be useful in demonstrating the API.

    """

    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': MonthlyWeatherByCity.objects.all()
                },
                'terms': [
                    'month',
                    'boston_temp'
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
                    'type': 'pie',
                    'stacking': False
                },
                'terms': {
                    'month': ['boston_temp']
                }
            }],
            chart_options={
                'title': {
                    'text': 'Monthly Temperature of Boston'
                }
            },
            x_sortf_mapf_mts=(None, monthname, False)
    )
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': cht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def mapf_for_x(_, title, code, doc, sidebar_items):
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
    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': MonthlyWeatherByCity.objects.all()
                },
                'terms': [
                    'month',
                    'houston_temp',
                    'boston_temp'
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
                        'houston_temp'
                    ]
                }
            }],
            chart_options={
                'title': {
                    'text': 'Weather Data of Boston and Houston'
                },
                'xAxis': {
                    'title': {
                        'text': 'Month'
                    }
                }
            },
            x_sortf_mapf_mts=(None, monthname, False))
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': cht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def multi_table_same_x(_, title, code, doc, sidebar_items):
    """
    Data from multiple models on same chart
    ----------------------------------------

    This example demonstrates data from two different models
    ``MonthlyWeatherByCity`` and ``MonthlyWeatherSeattle`` on the same chart
    and on the same x-axis.

    Points to note:

    - The `month` in ``terms`` for seattle data is written as
      ``{'month_seattle': 'month'}`` instead of as just ``'month'`` because
      in the latter case it would overwrite the ``'month'`` term from the
      other model.
    - Notice that the Seattle weather data in the database does not have any
      data for August (8) and September (9). Chartit gracefully skips them
      and plots the rest of the data points aligned correctly.
    """
    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': MonthlyWeatherByCity.objects.all()
                },
                'terms': [
                    'month',
                    'houston_temp',
                    'boston_temp'
                ]}, {
                'options': {
                    'source': MonthlyWeatherSeattle.objects.all()
                },
                'terms': [
                    {'month_seattle': 'month'},
                    'seattle_temp'
                ]}
             ]
    )

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
                        'houston_temp'],
                    'month_seattle': ['seattle_temp']
                }
            }],
            chart_options={
                'title': {
                    'text': 'Weather by Month (from 2 different tables)'},
                'xAxis': {
                    'title': {
                        'text': 'Month number'
                    }
                }
            }
    )
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': cht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def multi_axes_and_types(_, title, code, doc, sidebar_items):
    """
    Charts on multiple axes and multiple chart types
    -------------------------------------------------

    This example demonstrates how to plot data on different axes using
    different chart types.

    Points to note:

    - You can plot data on different axes by setting the ``xAxis`` and
      ``yAxis``.
    - The ``series_options`` - ``options`` dict takes any of the values from
      `Highcharts series options
      <http://api.highcharts.com/highcharts#Series>`_
    - If there are only 2 axes (0 and 1), the default behavior of Chartit is
      to display them on opposite sides. You can override this default behavior
      by setting ``{"opposite": False}`` manually. If there are more than
      2 axes, Chartit displays all of them on the same side by default.
    """
    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': MonthlyWeatherByCity.objects.all()
                },
                'terms': [
                    'month',
                    'houston_temp',
                    'boston_temp'
                ]
            }]
    )

    cht = Chart(
            datasource=ds,
            series_options=[{
                'options': {
                    'type': 'line',
                    'xAxis': 0,
                    'yAxis': 0,
                    'zIndex': 1
                },
                'terms': {
                    'month': ['boston_temp']
                }}, {
                'options': {
                    'type': 'area',
                    'xAxis': 1,
                    'yAxis': 1
                },
                'terms': {
                    'month': ['houston_temp']
                }
            }],
            chart_options={
                'title': {
                    'text': 'Weather Data by Month (on different axes)'
                },
                'xAxis': {
                    'title': {
                        'text': 'Month number'
                    }
                }
            }
    )
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': cht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def chart_default_options(_, title, code, doc, sidebar_items):
    """
    Some default options explained
    -------------------------------

    Even though the ``chart_options`` are not specified, Chartit
    automatically tries to guess the axis titles, chart titles etc.

    Points to note:

    - Notice how the axes are named, chart is named etc. by default.
    """
    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': MonthlyWeatherByCity.objects.all()
                },
                'terms': [
                    'month',
                    'houston_temp',
                    'boston_temp'
                ]}, {
                'options': {
                    'source': MonthlyWeatherSeattle.objects.all()
                },
                'terms': [
                    {'month_seattle': 'month'},
                    'seattle_temp'
                ]}
            ]
    )

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
                        'houston_temp'
                    ],
                    'month_seattle': ['seattle_temp']
                }
            }]
    )
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': cht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def scatter_plot(_, title, code, doc, sidebar_items):
    """
    Scatter Plot
    -------------

    The ``DailyWeather`` database has data by ``month``, ``day``, ``city`` and
    ``temperature``. In this example we plot a scatter plot of temperature
    of the city of Boston w.r.t month.

    Points to note:

    - Notice that the data is filtered naturally using ``filter`` method in
      django.

    """
    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': DailyWeather.objects.filter(city="Boston")
                },
                'terms': [
                    'month',
                    'temperature'
                ]
            }]
    )

    cht = Chart(
            datasource=ds,
            series_options=[{
                'options': {
                    'type': 'scatter'
                },
                'terms': {
                    'month': ['temperature']
                }
            }],
            chart_options={
                'title': {
                    'text': 'Boston weather scatter plot'
                },
                'xAxis': {
                    'title': {
                       'text': 'Month'
                    }
                }
            }
    )
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': cht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def combination_plot(_, title, code, doc, sidebar_items):
    """
    Combination Plot
    -----------------

    We can do more complicated plots from multiple databases on the same chart.
    In this chart we plot a scatter plot of daily weather of Boston from the
    ``DailyWeather`` database and the monthly average temperature of Boston as
    a from the ``MonthlyWeatherByCity`` database on the same chart.

    Points to note:

    - Notice that the data is filtered naturally using ``filter`` method in
      django.
    - The ``zIndex`` parameter (one of the many
      `Highcharts series options <http://www.highcharts.com/ref/#series>`_) is
      used to force the monthly temperature to be on the top.
    """
    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': DailyWeather.objects.filter(city="Boston")
                },
                'terms': [
                    'month',
                    'temperature'
                ]}, {
                'options': {
                    'source': MonthlyWeatherByCity.objects.all()
                },
                'terms': [
                    {'month_boston': 'month'},
                    'boston_temp'
                ]}
            ]
    )

    cht = Chart(
            datasource=ds,
            series_options=[{
                'options': {
                    'type': 'scatter'
                },
                'terms': {
                    'month': ['temperature']
                }}, {
                'options': {
                    'type': 'scatter',
                    'zIndex': 1
                },
                'terms': {
                    'month_boston': ['boston_temp']
                }},
            ],
            chart_options={
                'title': {
                    'text': 'Boston Daily weather and Monthly Average'
                },
                'yAxis': {
                    'title': {
                        'text': 'Temperature'
                    }
                }
            }
    )
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': cht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def column_chart_multi_stack(_, title, code, doc, sidebar_items):
    """
    Column Chart
    ------------------
    Column chart of temperatures of Boston and New York in one stack and the
    temperature of Houston in another stack.

    Points to note:

    - Notice that ``houston_temp`` shares all the other options with
      ``boston_temp`` and ``new_york_temp``. So we override just the ``stack``
      parameter from the ``options`` for ``houston_temp`` by writing
      ``{'houston_temp: {'stack': 1}}``.

      We can also write ``series_options`` as ::

        series_options = [
               {'options':{
                  'type': 'column',
                  'stacking': True,
                  'stack': 0},
                'terms':{
                  'month': [
                    'boston_temp',
                    'new_york_temp']}},

               {'options':{
                  'type': 'column',
                  'stacking': True,
                  'stack': 1},
                'terms':{
                  'month': [
                    'houston_temp']}
                    }]

      to plot this chart. But the form used in the code is much shorter and
      there is less duplication.

    Note: This demo is to demonstrate the use of the API and not to teach
    you data analysis and data presentation skills. Not all charts plotted
    in this demo may make sense in real life applications. But they can
    still be useful in demonstrating the API.
    """

    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': MonthlyWeatherByCity.objects.all()
                },
                'terms': [
                    'month',
                    'houston_temp',
                    'boston_temp',
                    'new_york_temp'
                ]
            }]
    )

    cht = Chart(
            datasource=ds,
            series_options=[{
                'options': {
                    'type': 'column',
                    'stacking': True,
                    'stack': 0
                },
                'terms': {
                    'month': [
                        'boston_temp',
                        'new_york_temp',
                        {
                            'houston_temp': {
                                'stack': 1
                            }
                        },
                    ]
                }
            }],
            chart_options={
                'title': {
                    'text': 'Weather Data of Boston, New York and Houston'
                },
                'xAxis': {
                    'title': {
                        'text': 'Month number'
                    }
                }
            }
    )
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': cht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def column_chart(_, title, code, doc, sidebar_items):
    """
    Column Chart
    ------------------
    Just a simple column chart of temperatures of Boston and Houston stacked
    on top of each other.

    Points to note:

    - Any of the `Highcharts series options
      <http://api.highcharts.com/highcharts#Series>`_ are valid options for
      the Chart
      ``series_options`` - ``options`` dict. In this case we set the
      ``stacking`` parameter to ``True`` to stack the columns on the top of
      each other.

    Note: This demo is to demonstrate the use of the API and not to teach
    you data analysis and data presentation skills. Not all charts plotted
    in this demo may make sense in real life applications. But they can
    still be useful in demonstrating the API.
    """

    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': MonthlyWeatherByCity.objects.all()
                },
                'terms': [
                    'month',
                    'houston_temp',
                    'boston_temp'
                ]
            }]
    )

    cht = Chart(
            datasource=ds,
            series_options=[{
                'options': {
                    'type': 'column',
                    'stacking': True},
                'terms': {
                    'month': [
                        'boston_temp',
                        'houston_temp'
                    ]
                }
            }],
            chart_options={
                'title': {
                    'text': 'Weather Data of Boston and Houston'
                },
                'xAxis': {
                    'title': {
                        'text': 'Month number'
                    }
                }
            }
    )
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': cht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def combination_line_pie(_, title, code, doc, sidebar_items):
    """
    Combination of line and Pie charts
    -----------------------------------
    A combination of line and pie charts displayed on the same chart.

    Points to note:

    - ``center`` and ``size`` are used to center the pie chart and scale it
      to fit in the chart. Remember that any of the `Highcharts series options
      <http://api.highcharts.com/highcharts#Series>`_ are valid options for
      the Chart ``series_options`` - ``options`` dict.

    Note: This demo is to demonstrate the use of the API and not to teach
    you data analysis and data presentation skills. Not all charts plotted
    in this demo may make sense in real life applications. But they can
    still be useful in demonstrating the API.
    """

    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': MonthlyWeatherByCity.objects.all()
                },
                'terms': [
                    'month',
                    'boston_temp',
                    'houston_temp'
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
                    'type': 'line'
                },
                'terms': {
                    'month': ['boston_temp']
                }}, {
                'options': {
                    'type': 'pie',
                    'center': [150, 100],
                    'size': '50%'
                },
                'terms': {
                    'month': ['houston_temp']
                }}
            ],
            chart_options={
                'title': {
                    'text': 'Weather Data of Boston (line) and Houston (pie)'
                }
            },
            x_sortf_mapf_mts=[(None, monthname, False),
                              (None, monthname, False)])
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': cht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def basicline_with_datefield(_, title, code, doc, sidebar_items):
    """
    A Basic Line Chart with DateField
    ---------------------------------
    This chart plots sales quantities per day from the first book store.

    Points to note:

    - ``sale_date`` is a DateField

    """

    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': SalesHistory.objects.filter(
                                            bookstore=BookStore.objects.first()
                              )[:10]
                },
                'terms': [
                    'sale_date',
                    'sale_qty',
                ]
            }]
    )

    cht = Chart(
            datasource=ds,
            series_options=[{
                'options': {
                    'type': 'line',
                    'stacking': False
                },
                'terms': {
                    'sale_date': [
                        'sale_qty',
                    ]
                }
            }],
            chart_options={
                'title': {
                    'text': 'Sales QTY per day'
                },
                'xAxis': {
                    'title': {
                        'text': 'Sale date'
                    }
                }
            }
    )
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': cht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def datetimefield_from_related_model(_, title, code, doc, sidebar_items):
    """
    A Basic Line Chart with DateTimeField from related model
    --------------------------------------------------------
    This chart plots sales quantities from the first book store based on
    when the book was published.
    """

    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': SalesHistory.objects.filter(
                                            bookstore=BookStore.objects.first()
                              )[:10]
                },
                'terms': [
                    'book__published_at',
                    'sale_qty',
                ]
            }]
    )

    cht = Chart(
            datasource=ds,
            series_options=[{
                'options': {
                    'type': 'line',
                    'stacking': False
                },
                'terms': {
                    'book__published_at': [
                        'sale_qty',
                    ]
                }
            }],
            chart_options={
                'title': {
                    'text': 'Sales QTY vs. Book publish date'
                },
                'xAxis': {
                    'title': {
                        'text': 'Publish date'
                    }
                }
            }
    )
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': cht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def extra_datefield(_, title, code, doc, sidebar_items):
    """
    A Basic Line Chart using QuerySet.extra() with DateField
    --------------------------------------------------------
    This chart plots sales quantities per day from the first book store.
    We're using QuerySet.extra() to format the date value directly at
    the DB level.
    """

    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    # NOTE: strftime is SQLite function.
                    # For MySQL use DATE_FORMAT
                    'source': SalesHistory.objects.extra(
                                    select={
                                        'sold_at': \
                                        "strftime('%%Y/%%m/%%d', sale_date)"
                                    }
                              ).filter(
                                    bookstore=BookStore.objects.first()
                              )[:10]
                },
                'terms': [
                    'sold_at',
                    'sale_qty',
                ]
            }]
    )

    cht = Chart(
            datasource=ds,
            series_options=[{
                'options': {
                    'type': 'line',
                    'stacking': False
                },
                'terms': {
                    'sold_at': [
                        'sale_qty',
                    ]
                }
            }],
            chart_options={
                'title': {
                    'text': 'Sales QTY per day'
                },
                'xAxis': {
                    'title': {
                        'text': 'Sale date'
                    }
                }
            }
    )
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': cht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def avg_count(_, title, code, doc, sidebar_items):
    """
    A Basic Line Chart using Avg() and Count()
    ------------------------------------------
    This chart plots the average book rating in each genre
    together with the number of books in each genre.
    """

    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': Book.objects.values('genre').annotate(
                                Avg('rating'),
                                Count('genre')
                              )
                },
                'terms': [
                    'genre__name',
                    'rating__avg',
                    'genre__count'
                ]
            }]
    )

    cht = Chart(
            datasource=ds,
            series_options=[{
                'options': {
                    'type': 'line',
                    'stacking': False
                },
                'terms': {
                    'genre__name': [
                        'rating__avg', 'genre__count'
                    ]
                }
            }],
            chart_options={
                'title': {
                    'text': 'Book rating and count per Genre'
                },
                'xAxis': {
                    'title': {
                        'text': 'Genre'
                    }
                }
            }
    )
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': cht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def model_property(request, title, code, doc, sidebar_items):
    """
    A basic Chart using model property
    ----------------------------------


    NOTE that ``region()`` is a model property defined as

    ::

        class City(models.Model):
            def region(self):
                return 'USA:%s' % self.city
    """

    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': SalesHistory.objects.only(
                                'bookstore__city', 'sale_qty'
                              )[:10],
                },
                'terms': [
                    'bookstore__city__region',
                    'sale_qty'
                ]
            }]
    )

    cht = Chart(
            datasource=ds,
            series_options=[{
                'options': {
                    'type': 'column',
                    'stacking': False,
                    'stack': 0,
                },
                'terms': {
                    'bookstore__city__region': [
                        'sale_qty'
                    ]
                }},
            ],
            chart_options={
                'title': {
                    'text': 'Sales reports'
                },
                'xAxis': {
                    'title': {
                        'text': 'City'
                    }
                }
            }
    )
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': cht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})
