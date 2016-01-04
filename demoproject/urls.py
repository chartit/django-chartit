from django.conf.urls.defaults import patterns
from django.views.generic.simple import redirect_to

home_view_title = [
    (r'demo/', 'demohome',
     'Hello there!'),
]

chart_view_title = [
    (r'demo/chart/model-details/', 'model_details',
     'Model Details'),
    (r'demo/chart/basic-line/', 'basicline',
     'Line chart'),
    (r'demo/chart/mapf-for-x/', 'mapf_for_x',
     'Custom names for x-axis values'),
    (r'demo/chart/column-chart/', 'column_chart',
     'Column chart'),
    (r'demo/chart/column-chart-multi-stack/', 'column_chart_multi_stack',
     'Column chart with multiple stacks'),
    (r'demo/chart/scatter-plot/', 'scatter_plot',
     'Scatter plot'),
    (r'demo/chart/basic-pie/', 'basicpie',
     'Pie chart'),
    (r'demo/chart/multi-table-same-x/', 'multi_table_same_x',
     'Data from multiple models on same chart'),
    (r'demo/chart/multi-axes-and-types/', 'multi_axes_and_types',
     'Multiple chart types and multiple axes'),
    (r'demo/chart/chart-default-options/', 'chart_default_options',
     'Chart default options explained'),
    (r'demo/chart/combination-plot/', 'combination_plot',
     'Scatter plot with data from multiple models'),
    (r'demo/chart/combination-line-pie/', 'combination_line_pie',
     'Combination of line and pie'),
]

pivot_view_title = [
    (r'demo/pivot/model-details/', 'model_details',
     'Model Details'),
    (r'demo/pivot/simple/', 'simplepivot',
     'A basic Pivot Chart'),
    (r'demo/pivot/pivot-with-legend/', 'pivot_with_legend',
     'Pivot chart with legend by'),
    (r'demo/pivot/multi-category/', 'pivot_multi_category',
     'Pivot chart with multiple categories'),
    (r'demo/pivot/top-n-per-cat/', 'pivot_with_top_n_per_cat',
     'Pivot chart with top few items per category'),
    (r'demo/pivot/top-n/', 'pivot_top_n',
     'Pivot chart with only top few items'),
    (r'demo/pivot/pareto/', 'pivot_pareto',
     'Pareto Chart'),
    (r'demo/pivot/muti-axes/', 'pivot_multi_axes',
     'Pivot Chart on multiple axes'),
    (r'demo/pivot/mapf/', 'pivot_mapf',
     'Pivot Chart with custom mapping for x-axis')
]

home_sidebar = [(r'../' + url, title) for (url, view, title) in
                 home_view_title]

chart_sidebar = [(r'../' + url, title) for (url, view, title) in
                 chart_view_title]
pivot_sidebar = [(r'../' + url, title) for (url, view, title) in
                    pivot_view_title]

sidebar_items = [("Welcome", home_sidebar),
                 ("Charts", chart_sidebar),
                 ("Pivot Charts", pivot_sidebar)]

home_pattern_tuples = [(r'^' + url + r'$',
                       view,
                       {'title': title,
                        'sidebar_items': sidebar_items}) for
                           (url, view, title) in home_view_title]

chart_pattern_tuples = [(r'^' + url + r'$',
                       view,
                       {'title': title,
                        'sidebar_items': sidebar_items}) for
                           (url, view, title) in chart_view_title]
pivot_pattern_tuples = [(r'^' + url + r'$',
                       view,
                       {'title': title,
                        'sidebar_items': sidebar_items}) for
                           (url, view, title) in pivot_view_title]

homepatterns = patterns('homepage.views',
                        (r'^$', 'homepage'),)
homepatterns += patterns('',
                         (r'^favicon\.ico$',
                          'django.views.generic.simple.redirect_to',
                          {'url': '/static/home/images/favicon.ico'}))

demopatterns = patterns('demo.views', *home_pattern_tuples)
chartpatterns = patterns('chartdemo.views', *chart_pattern_tuples)
pivotpatterns = patterns('pivotdemo.views', *pivot_pattern_tuples)

urlpatterns = homepatterns + demopatterns + chartpatterns + pivotpatterns