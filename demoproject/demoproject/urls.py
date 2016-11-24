"""demoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views, chartdemo, pivotdemo, chartraw


sort_order = {
    'Welcome': 0,
    'Charts': 1,
    'Pivot Charts': 2,
    'Charts w/ RawQuerySet': 3,
}
sidebar_items = []

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^demo/$', views.demohome,
        {
            'title': 'Hello there!',
            'sidebar_section': 'Welcome',
        },
        name='demo_home',
        ),

    url(r'^demo/model-details/$', views.model_details,
        {
            'title': 'Model Details',
            'sidebar_section': 'Welcome',
        },
        name='model_details',
        ),

    # chart examples
    url(r'^demo/chart/basic-line/$', chartdemo.basicline,
        {
            'title': 'Line chart',
            'sidebar_section': 'Charts',
        },
        name='line_chart',
        ),

    url(r'^demo/chart/mapf-for-x/$', chartdemo.mapf_for_x,
        {
            'title': 'Custom names for x-axis values',
            'sidebar_section': 'Charts',
        },
        name='mapf_for_x',
        ),

    url(r'^demo/chart/column-chart/$', chartdemo.column_chart,
        {
            'title': 'Column chart',
            'sidebar_section': 'Charts',
        },
        name='column_chart',
        ),

    url(r'^demo/chart/column-chart-multi-stack/$',
        chartdemo.column_chart_multi_stack,
        {
            'title': 'Column chart with multiple stacks',
            'sidebar_section': 'Charts',
        },
        name='column_chart_multi_stack',
        ),

    url(r'^demo/chart/scatter-plot/$', chartdemo.scatter_plot,
        {
            'title': 'Scatter plot',
            'sidebar_section': 'Charts',
        },
        name='scatter_plot',
        ),

    url(r'^demo/chart/basic-pie/$', chartdemo.basicpie,
        {
            'title': 'Pie chart',
            'sidebar_section': 'Charts',
        },
        name='basic_pie',
        ),

    url(r'^demo/chart/multi-table-same-x/$', chartdemo.multi_table_same_x,
        {
            'title': 'Data from multiple models on same chart',
            'sidebar_section': 'Charts',
        },
        name='multiple_models_same_chart',
        ),

    url(r'^demo/chart/multi-axes-and-types/$', chartdemo.multi_axes_and_types,
        {
            'title': 'Multiple chart types and multiple axes',
            'sidebar_section': 'Charts',
        },
        name='multiple_models_multiple_axes',
        ),

    url(r'^demo/chart/chart-default-options/$',
        chartdemo.chart_default_options,
        {
            'title': 'Chart default options explained',
            'sidebar_section': 'Charts',
        },
        name='chart_default_options_explained',
        ),

    url(r'^demo/chart/combination-plot/$', chartdemo.combination_plot,
        {
            'title': 'Scatter plot with data from multiple models',
            'sidebar_section': 'Charts',
        },
        name='scatter_plot_multiple_models',
        ),

    url(r'^demo/chart/combination-line-pie/$', chartdemo.combination_line_pie,
        {
            'title': 'Combination of line and pie',
            'sidebar_section': 'Charts',
        },
        name='line_pie_combination',
        ),

    url(r'^demo/chart/line-with-datefield/$',
        chartdemo.basicline_with_datefield,
        {
            'title': 'Line chart with DateField field',
            'sidebar_section': 'Charts',
        },
        name='line_datefield',
        ),

    url(r'^demo/chart/datetime-from-related/$',
        chartdemo.datetimefield_from_related_model,
        {
            'title': 'Chart with DateTimeField from related model',
            'sidebar_section': 'Charts',
        },
        name='line_datetime_related',
        ),

    url(r'^demo/chart/extra-datefield/$', chartdemo.extra_datefield,
        {
            'title': 'Line chart with extra() DateField',
            'sidebar_section': 'Charts',
        },
        name='line_extra_datefield',
        ),

    url(r'^demo/chart/avg-count/$', chartdemo.avg_count,
        {
            'title': 'Line chart with Avg() and Count()',
            'sidebar_section': 'Charts',
        },
        name='line_avg_count',
        ),

    url(r'^demo/chart/model-property/$', chartdemo.model_property,
        {
            'title': 'Line chart using model property',
            'sidebar_section': 'Charts',
        },
        name='line_model_property',
        ),

    # pivot chart examples
    url(r'^demo/pivot/simple/$', pivotdemo.simplepivot,
        {
            'title': 'A basic Pivot Chart',
            'sidebar_section': 'Pivot Charts',
        },
        name='pivot_basic_chart',
        ),

    url(r'^demo/pivot/pivot-with-legend/$', pivotdemo.pivot_with_legend,
        {
            'title': 'Pivot chart with legend by',
            'sidebar_section': 'Pivot Charts',
        },
        name='pivot_chart_legend_by',
        ),

    url(r'^demo/pivot/multi-category/$', pivotdemo.pivot_multi_category,
        {
            'title': 'Pivot chart with multiple categories',
            'sidebar_section': 'Pivot Charts',
        },
        name='pivot_multiple_categories',
        ),

    url(r'^demo/pivot/top-n-per-cat/$', pivotdemo.pivot_with_top_n_per_cat,
        {
            'title': 'Pivot chart with top few items per category',
            'sidebar_section': 'Pivot Charts',
        },
        name='pivot_top_few_per_category',
        ),

    url(r'^demo/pivot/top-n/$', pivotdemo.pivot_top_n,
        {
            'title': 'Pivot chart with only top few items',
            'sidebar_section': 'Pivot Charts',
        },
        name='pivot_chart_top_few_items_only',
        ),

    url(r'^demo/pivot/pareto/$', pivotdemo.pivot_pareto,
        {
            'title': 'Pareto Chart',
            'sidebar_section': 'Pivot Charts',
        },
        name='pivot_pareto',
        ),

    url(r'^demo/pivot/muti-axes/$', pivotdemo.pivot_multi_axes,
        {
            'title': 'Pivot Chart on multiple axes',
            'sidebar_section': 'Pivot Charts',
        },
        name='pivot_chart_multiple_axes',
        ),

    url(r'^demo/pivot/mapf/$', pivotdemo.pivot_mapf,
        {
            'title': 'Pivot Chart with custom mapping for x-axis',
            'sidebar_section': 'Pivot Charts',
        },
        name='pivot_chart_custom_x_axes_mapping',
        ),

    url(r'^demo/pivot/pivot-datefield/$', pivotdemo.pivot_with_datefield,
        {
            'title': 'Pivot Chart with DateField',
            'sidebar_section': 'Pivot Charts',
        },
        name='pivot_chart_datefield',
        ),

    url(r'^demo/pivot/pivot-datetime-related/$',
        pivotdemo.pivot_datetime_related,
        {
            'title': 'Pivot Chart with DateTimeField from related model',
            'sidebar_section': 'Pivot Charts',
        },
        name='pivot_chart_datetime_related',
        ),

    # chart examples with RawQuerySet
    url(r'^demo/chart-raw/basic-line/$', chartraw.basicline,
        {
            'title': 'Line chart',
            'sidebar_section': 'Charts w/ RawQuerySet',
        },
        name='raw_line_chart',
        ),

    url(r'^demo/chart-raw/mapf-for-x/$', chartraw.mapf_for_x,
        {
            'title': 'Custom names for x-axis values',
            'sidebar_section': 'Charts w/ RawQuerySet',
        },
        name='raw_mapf_for_x',
        ),


    url(r'^demo/chart-raw/multi-table-same-x/$', chartraw.multi_table_same_x,
        {
            'title': 'Multiple sources on same chart',
            'sidebar_section': 'Charts w/ RawQuerySet',
        },
        name='raw_multiple_models_same_chart',
        ),

    url(r'^demo/chart-raw/line-with-datefield/$',
        chartraw.basicline_with_datefield,
        {
            'title': 'Line chart with DateField field',
            'sidebar_section': 'Charts w/ RawQuerySet',
        },
        name='raw_line_datefield',
        ),

    url(r'^demo/chart-raw/datetime-from-related/$',
        chartraw.datetimefield_from_related_model,
        {
            'title': 'DateTimeField from related model',
            'sidebar_section': 'Charts w/ RawQuerySet',
        },
        name='raw_line_datetime_related',
        ),

    url(r'^demo/chart-raw/extra-datefield/$', chartraw.extra_datefield,
        {
            'title': 'Extra DateField in SQL',
            'sidebar_section': 'Charts w/ RawQuerySet',
        },
        name='raw_line_extra_datefield',
        ),

    url(r'^demo/chart-raw/avg-count/$', chartraw.avg_count,
        {
            'title': 'Line chart with Avg() and Count()',
            'sidebar_section': 'Charts w/ RawQuerySet',
        },
        name='raw_line_avg_count',
        ),
]

# build sidebar_items first
seen_sections = []
for u in urlpatterns:
    if u.default_args:
        section = u.default_args['sidebar_section']
        title = u.default_args['title']

        # check if we've seen this section already
        if section not in seen_sections:
            item = {
                'sort_order': sort_order[section],
                'section': section,
                'links': [],
            }
            sidebar_items.append(item)
            seen_sections.append(section)

        # now add the new link to the sidebar section
        for item in sidebar_items:
            if item['section'] == section:
                item['links'].append((title, u.name))
                break

        del u.default_args['sidebar_section']

# now assign sidebar_items to urls
for u in urlpatterns:
    if u.default_args:
        u.default_args['sidebar_items'] = sidebar_items
