from django.conf.urls.defaults import patterns

url_view_title = [
    (r'simple/basic-line', 'basicline', 
     'A simple line chart'),
    (r'simple/line-with-mapf-for-x', 'line_with_mapf_for_x',
     'Mapping custom names to the x-axis'),
    (r'simple/line-multi-table-same-x', 'line_multi_table_same_x', 
     'Data from multiple models on same x-axis' ),
]

sidebar_items = [(r'../' + url, title) for (url, view, title) in url_view_title]

url_pattern_tuples = [(r'^' + url + r'$', 
                       view, 
                       {'title': title, 
                        'sidebar_items': sidebar_items}) for 
                           (url, view, title) in url_view_title]
                           
urlpatterns = patterns('simpleweather.views', *url_pattern_tuples)