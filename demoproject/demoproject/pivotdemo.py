from django.db.models import Sum, Avg
from chartit import PivotChart, PivotDataPool
from django.shortcuts import render_to_response
from .decorators import add_source_code_and_doc
from .models import SalesHistory, Book


@add_source_code_and_doc
def simplepivot(_, title, code, doc, sidebar_items):
    """
    A simple pivot chart.

    Points to notice:

    - You can use the default django convention of double underscore (__) to
      *follow* to the fields in different models.
    """
    # start_code
    ds = PivotDataPool(
          series=[
           {'options': {
              'source': SalesHistory.objects.all(),
              'categories': 'bookstore__city__city'},
            'terms': {
              'tot_sales': Sum('sale_qty')}}])

    pivcht = PivotChart(
              datasource=ds,
              series_options=[
                {'options': {
                   'type': 'column'},
                 'terms': ['tot_sales']}])
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': pivcht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def pivot_with_legend(_, title, code, doc, sidebar_items):
    """
    Pivot Chart with legend by field. This pivot chart plots total sale
    quantity of books in each city legended by the book genre name.
    """
    # start_code
    ds = PivotDataPool(
          series=[
           {'options': {
              'source': SalesHistory.objects.all(),
              'categories': 'bookstore__city__city',
              'legend_by': 'book__genre__name'},
            'terms': {
              'tot_sales': Sum('sale_qty')}}])

    pivcht = PivotChart(
              datasource=ds,
              series_options=[
                {'options': {
                   'type': 'column',
                   'stacking': True,
                   'xAxis': 0,
                   'yAxis': 0},
                 'terms': ['tot_sales']}])
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': pivcht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def pivot_multi_category(_, title, code, doc, sidebar_items):
    """
    Pivot Chart with multiple categories. In this chart the total sale
    quantity is plotted with respect to state and city.

    Points to note:

    - You can add any number of categories and legend_by entries in a list.
    - **Order matters**! Retrieving state and then city may yield different
      results compared to retrieving city and state depending on what you
      are trying to plot.
    """
    # start_code
    ds = PivotDataPool(
          series=[
           {'options': {
              'source': SalesHistory.objects.all(),
              'categories': [
                'bookstore__city__state',
                'bookstore__city__city'],
              'legend_by': 'book__genre__name'},
            'terms': {
              'tot_sales': Sum('sale_qty')}}])

    pivcht = PivotChart(
              datasource=ds,
              series_options=[
                {'options': {
                   'type': 'column',
                   'stacking': True,
                   'xAxis': 0,
                   'yAxis': 0},
                 'terms': ['tot_sales']}])
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': pivcht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def pivot_with_top_n_per_cat(_, title, code, doc, sidebar_items):
    """
    Pivot Chart each category limited to a select top items.

    Points to note:

    - These charts are helpful when there are too many items in each category
      and we only want to focus on the top few items in each category.
    """
    # start_code
    ds = PivotDataPool(
          series=[
           {'options': {
              'source': SalesHistory.objects.all(),
              'categories': [
                'bookstore__city__state',
                'bookstore__city__city'],
              'legend_by': 'book__genre__name',
              'top_n_per_cat': 2},
            'terms': {
              'tot_sales': Sum('sale_qty')}}])

    pivcht = PivotChart(
              datasource=ds,
              series_options=[
                {'options': {
                   'type': 'column',
                   'stacking': True,
                   'xAxis': 0,
                   'yAxis': 0},
                 'terms': ['tot_sales']}])
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': pivcht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def pivot_top_n(_, title, code, doc, sidebar_items):
    """
    Pivot Chart limited to top few items. In this chart the sales quanity is
    plotted w.r.t state/city but the chart is limited to only top 5 cities
    witht the highest sales.

    Points to note:

    - These charts are helpful in cases where there is a long *tail* and we
      only are interested in the top few items.
    - ``top_n_term`` is always required. If there are multiple items, it will
      elimnate confusion regarding what the term the chart needs to be
      limited by.
    """
    # start_code
    ds = PivotDataPool(
          series=[
           {'options': {
              'source': SalesHistory.objects.all(),
              'categories': [
                'bookstore__city__state',
                'bookstore__city__city'],
              'legend_by': 'book__genre__name'},
            'terms': {
              'tot_sales': Sum('sale_qty')}}],
          top_n=5,
          top_n_term='tot_sales')

    pivcht = PivotChart(
              datasource=ds,
              series_options=[
                {'options': {
                   'type': 'column',
                   'stacking': True,
                   'xAxis': 0,
                   'yAxis': 0},
                 'terms': ['tot_sales']}])
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': pivcht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def pivot_pareto(_, title, code, doc, sidebar_items):
    """
    Pivot Chart plotted as a `pareto chart
    <http://en.wikipedia.org/wiki/Pareto_chart>`_ w.r.t the total sales
    quantity.
    """
    # start_code
    ds = PivotDataPool(
          series=[
           {'options': {
              'source': SalesHistory.objects.all(),
              'categories': [
                'bookstore__city__state',
                'bookstore__city__city'],
              'legend_by': 'book__genre__name'},
            'terms': {
              'tot_sales': Sum('sale_qty')}}],
          top_n=5,
          top_n_term='tot_sales',
          pareto_term='tot_sales')

    pivcht = PivotChart(
              datasource=ds,
              series_options=[
                {'options': {
                   'type': 'column',
                   'stacking': True,
                   'xAxis': 0,
                   'yAxis': 0},
                 'terms': ['tot_sales']}])
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': pivcht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def pivot_multi_axes(_, title, code, doc, sidebar_items):
    """
    Pivot Chart with multiple terms on multiple axes.

    Points to note:

    - Note that the term ``avg-price`` is passed as a dict (instead of as a
      django aggregate to allow us to override the default ``legend_by``
      option. When passed as a dict, the aggregate function needs to be passed
      to the ``func`` key.
    - Alternatively this could be written as ::

        series= [
           {'options':{
              'source': SalesHistory.objects.all(),
              'categories': [
                'bookstore__city__state',
                'bookstore__city__city'],
              'legend_by': 'book__genre__name'},
            'terms': {
              'tot_sales':Sum('sale_qty')}},

           {'options':{
              'source': SalesHistory.objects.all(),
              'categories': [
                'bookstore__city__state',
                'bookstore__city__city']},
            'terms': {
              'avg_price':Avg('price')}}
              ]

      but the one used in the code is more succint and has less duplication.
    """
    # start_code
    ds = PivotDataPool(
          series=[
           {'options': {
              'source': SalesHistory.objects.all(),
              'categories': [
                'bookstore__city__state',
                'bookstore__city__city'],
              'legend_by': 'book__genre__name'},
            'terms': {
              'tot_sales': Sum('sale_qty'),
              'avg_price': {
                'func': Avg('price'),
                'legend_by': None}}}],
          top_n=5,
          top_n_term='tot_sales',
          pareto_term='tot_sales')

    pivcht = PivotChart(
              datasource=ds,
              series_options=[
                {'options': {
                   'type': 'column',
                   'stacking': True},
                 'terms': [
                    'tot_sales',
                    {'avg_price': {
                        'type': 'line',
                        'yAxis': 1}}]}],
              chart_options={
                'yAxis': [{}, {'opposite': True}]})
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': pivcht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def pivot_mapf(_, title, code, doc, sidebar_items):
    """
    Pivot Chart with ``sortf_mapf_mts`` defined to map custom names for x-axis
    and to customize the x-axis sorting. In this chart we would like to plot
    region:city instead of state:city. However region is not available in the
    database. So custom mapf function comes to the rescue.

    Points to note:

    - Note that ``mapf`` receives a tuple and returns a tuple. This is true
      even when ``categories`` is a single element.
    - ``mts=True`` causes the elements to be mapped and then sorted. So all the
      N region cities are on the left and the S region cities are on the right
      hand side of the plot.
    """
    # start_code
    def region_state(x):
        region = {'CA': 'S', 'MA': 'N', 'TX': 'S', 'NY': 'N'}
        return (region[x[0]], x[1])

    ds = PivotDataPool(
          series=[
           {'options': {
              'source': SalesHistory.objects.all(),
              'categories': [
                'bookstore__city__state',
                'bookstore__city__city'],
              'legend_by': 'book__genre__name'},
            'terms': {
              'tot_sales': Sum('sale_qty')}}],
          sortf_mapf_mts=(None, region_state, True))

    pivcht = PivotChart(
              datasource=ds,
              series_options=[
                {'options': {
                   'type': 'column',
                   'stacking': True},
                 'terms': [
                    'tot_sales']}])
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': pivcht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def pivot_with_datefield(_, title, code, doc, sidebar_items):
    """
    Pivot chart with DateField
    --------------------------
    This chart shows total sales of one book per date.

    Note that we filter down the possible values using date range
    queries instead of slicing. Slicing the query results in an error.
    Slicing in Chart() charts however is fine!
    """
    # start_code
    ds = PivotDataPool(
          series=[
           {'options': {
              'source': SalesHistory.objects.filter(
                            book=Book.objects.filter(title="Hyperspace"),
                            sale_date__year=2010,
                            sale_date__month=10,
                        ),
              'categories': 'sale_date'},
            'terms': {
              'tot_sales': Sum('sale_qty')}}])

    pivcht = PivotChart(
              datasource=ds,
              series_options=[
                {'options': {
                   'type': 'column'},
                 'terms': ['tot_sales']}])
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': pivcht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})


@add_source_code_and_doc
def pivot_datetime_related(_, title, code, doc, sidebar_items):
    """
    Pivot chart with DateTimeField from related model
    -------------------------------------------------
    This chart shows total sales based on when book was published.
    The data is limited to books published during
    June 1st-20th, 2010 for brevity.

    Note that we filter down the possible values using date range
    queries instead of slicing. Slicing the query results in an error.
    Slicing in Chart() charts however is fine!
    """
    # start_code
    ds = PivotDataPool(
            series=[{
                'options': {
                    'source': SalesHistory.objects.filter(
                                book__published_at__year=2010,
                                book__published_at__month=6,
                              ),
                    'categories': 'book__published_at',
                    'legend_by': 'book__title',
                },
                'terms': {
                    'tot_sales': Sum('sale_qty'),
                }
            }]
    )

    pivcht = PivotChart(
        datasource=ds,
        series_options=[{
            'options': {
                'type': 'column',
                'stacking': True,
                'xAxis': 0,
                'yAxis': 0,
            },
            'terms': ['tot_sales']
        }]
    )
    # end_code
    return render_to_response('chart_code.html',
                              {
                                'chart_list': pivcht,
                                'code': code,
                                'title': title,
                                'doc': doc,
                                'sidebar_items': sidebar_items})
