"""
    Chart demos using RawQuerySet
"""
from chartit import DataPool, Chart
from django.shortcuts import render_to_response
from .decorators import add_source_code_and_doc
from .models import MonthlyWeatherByCity, MonthlyWeatherSeattle
from .models import SalesHistory, BookStore, Book


@add_source_code_and_doc
def basicline(_, title, code, doc, sidebar_items):
    """
    A Basic Line Chart
    ------------------
    This is just a simple line chart with data from 2 different columns using
    a ``RawQuerySet`` source.
    """

    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': MonthlyWeatherByCity.objects.raw(
                                "SELECT id, month, houston_temp, boston_temp "
                                "FROM demoproject_monthlyweatherbycity")
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
                    'source': MonthlyWeatherByCity.objects.raw(
                              "SELECT * FROM demoproject_monthlyweatherbycity"
                              )
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
    and on the same x-axis. Notice that we've mixed ``RawQuerySet`` and
    ``QuerySet`` sources together!
    """
    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': MonthlyWeatherByCity.objects.raw(
                              "SELECT * FROM demoproject_monthlyweatherbycity"
                              )
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
                    'source': SalesHistory.objects.raw(
                                "SELECT * FROM demoproject_saleshistory "
                                "WHERE bookstore_id=%s LIMIT 10",
                                [BookStore.objects.first().pk]
                              )
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
                    'source': SalesHistory.objects.raw(
                                "SELECT * FROM demoproject_saleshistory "
                                "WHERE bookstore_id=%s LIMIT 10",
                                [BookStore.objects.first().pk]
                              )
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
    A Basic Line Chart using extra DateField, not defined in the model
    ------------------------------------------------------------------
    This chart plots sales quantities per day from the first book store.
    In the ``RawQuerySet`` we select extra fields, which are not defined
    inside the model.
    """

    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    # NOTE: strftime is SQLite function.
                    # For MySQL use DATE_FORMAT
                    'source': SalesHistory.objects.raw(
                                "SELECT id, sale_qty, "
                                "strftime('%%Y/%%m/%%d', sale_date) as sold_at"
                                " FROM demoproject_saleshistory "
                                "WHERE bookstore_id=%s LIMIT 10",
                                [BookStore.objects.first().pk]
                              )

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
    A Basic Line Chart using AVG and COUNT
    --------------------------------------
    This chart plots the average book rating in each genre
    together with the number of books in each genre.

    NOTE that we use the SQL functions for average and count!
    """

    # start_code
    ds = DataPool(
            series=[{
                'options': {
                    'source': Book.objects.raw(
                                "SELECT "
                                "    demoproject_book.id, "
                                "    demoproject_genre.name as genre_name, "
                                "    avg(rating) as rating_avg, "
                                "    count(genre_id) as genre_count "
                                "FROM demoproject_book "
                                "JOIN demoproject_genre ON "
                                "     genre_id == demoproject_genre.id "
                                "GROUP BY genre_id "
                              )
                },
                'terms': [
                    'genre_name',
                    'rating_avg',
                    'genre_count'
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
                    'genre_name': [
                        'rating_avg', 'genre_count'
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
