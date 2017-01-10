import sys
import copy
import warnings
from collections import defaultdict, OrderedDict
from itertools import groupby

from .utils import _getattr, RecursiveDefaultDict
from .validation import clean_pcso, clean_cso, clean_x_sortf_mapf_mts
from .exceptions import APIInputError
from .chartdata import PivotDataPool, DataPool
import json


# in Python 3 the standard str type is unicode and the
# unicode type has been removed so define the keyword here
if sys.version_info.major >= 3:
    unicode = str


class BaseChart(object):
    """
        Common ancestor class for all charts to avoid code duplication.
    """
    def __init__(self):
        self.hcoptions = RecursiveDefaultDict({})
        self.PY2 = sys.version_info.major == 2

    def to_json(self):
        """Load Chart's data as JSON
        Useful in Ajax requests. Example:

        Return JSON from this method and response to client::

            return JsonResponse(cht.to_json(), safe=False)

        Then use jQuery load data and create Highchart::

            $(function(){
            $.getJSON("/data",function(data){
                $('#container').highcharts(JSON.parse(data));
                });
            });
        """
        return json.dumps(self.hcoptions)


class Chart(BaseChart):

    def __init__(self, datasource, series_options, chart_options=None,
                 x_sortf_mapf_mts=None):
        """Chart accept the datasource and some options to create the chart and
        creates it.

        **Arguments**:

        - **datasource** (**required**) - a ``DataPool`` object that holds the
          terms and other information to plot the chart from.

        - **series_options** (**required**) - specifies the options to plot
          the terms on the chart. It is of the form ::

            [{'options': {
                #any items from HighChart series. For ex.,
                'type': 'column'
               },
               'terms': {
                 'x_name': ['y_name',
                            {'other_y_name': {
                               #overriding options}},
                            ...],
                 ...
                 },
               },
              ... #repeat dicts with 'options' & 'terms'
              ]

          Where -

          - **options** (**required**) - a ``dict``. Any of the parameters
            from the `Highcharts options object - series array
            <http://www.highcharts.com/ref/#series>`_ are valid as entries in
            the ``options`` dict except ``data`` (because data array is
            generated from your datasource by chartit). For example, ``type``,
            ``xAxis``, etc. are all valid entries here.

            .. note:: The items supplied in the options dict are not validated
               to make sure that Highcharts actually supports them. Any
               invalid options are just passed to Highcharts JS which silently
               ignores them.

          - **terms** (**required**) - a ``dict``. keys are the x-axis terms
            and the values are lists of y-axis terms for that particular
            x-axis term. Both x-axis and y-axis terms must be present in the
            corresponding datasource, otherwise an APIInputError is raised.

            The entries in the y-axis terms list must either be a ``str`` or
            a ``dict``. If entries are dicts, the keys need to be valid y-term
            names and the values need to be any options to override the
            default options. For example, ::

              [{'options': {
                  'type': 'column',
                  'yAxis': 0},
                'terms': {
                  'city': [
                    'temperature',
                   {'rainfall': {
                      'type': 'line',
                      'yAxis': 1}}]}}]

            plots a column chart of city vs. temperature as a line chart on
            yAxis: 0 and city vs. rainfall as a line chart on yAxis: 1. This
            can alternatively be expressed as two separate entries: ::

              [{'options': {
                  'type': 'column',
                  'yAxis': 0},
                'terms': {
                  'city': [
                    'temperature']}},
               {'options': {
                  'type': 'line',
                  'yAxis': 1},
                'terms': {
                  'city': [
                    'rainfall']}}]

        - **chart_options** (*optional*) - a ``dict``. Any of the options from
          the `Highcharts options object <http://www.highcharts.com/ref/>`_
          are valid (except the options in the ``series`` array which are
          passed in the ``series_options`` argument. The following
          ``chart_options`` for example, set the chart title and the axes
          titles. ::

              {'chart': {
                 'title': {
                   'text': 'Weather Chart'}},
               'xAxis': {
                 'title': 'month'},
               'yAxis': {
                 'title': 'temperature'}}

          .. note:: The items supplied in the ``chart_options`` dict are not
             validated to make sure that Highcharts actually supports them.
             Any invalid options are just passed to Highcharts JS which
             silently ignores them.

        **Raises**:

        - ``APIInputError`` if any of the terms are not present in the
          corresponding datasource or if the ``series_options`` cannot be
          parsed.
        """
        super(Chart, self).__init__()
        if not isinstance(datasource, DataPool):
            raise APIInputError("%s must be an instance of DataPool."
                                % datasource)
        self.datasource = datasource
        self.series_options = clean_cso(series_options, self.datasource)
        self.x_sortf_mapf_mts = clean_x_sortf_mapf_mts(x_sortf_mapf_mts)
        self.x_axis_vqs_groups = self._groupby_x_axis_and_vqs()
        self._set_default_hcoptions(chart_options)
        self.generate_plot()

    def _groupby_x_axis_and_vqs(self):
        """
        Here is an example of what this function would return ::

            {
                0: {
                    0: {'month_seattle': ['seattle_temp']},
                    1: {'month': ['houston_temp', 'boston_temp']}
                }
            }

        In the above example,

        - the inner most dict keys ('month' and 'month_seattle') are on the
          same xAxis (xAxis 0), just groupped in 2 groups (0 and 1)
        - the inner most list values are from same ValueQuerySet (table)

        If you decide to display multiple chart types with multiple axes
        then the return value will look like this ::


            {
                0: {
                    0: {'month': ['boston_temp']}
                },
                1: {
                    0: {'month': ['houston_temp']}
                }
            }

        - the outer most 0 and 1 are the numbers of the x axes
        - the inner most 0 shows that each axis has 1 data group
        """
        def sort_fn(td_tk):
            return td_tk[1].get('xAxis', 0)

        def sort2_fn(td_tk):
            return dss[td_tk[1]['_x_axis_term']]['_data']

        dss = self.datasource.series
        x_axis_vqs_groups = defaultdict(dict)
        so = sorted(self.series_options.items(), key=sort_fn)
        x_axis_groups = groupby(so, sort_fn)
        for (x_axis, itr1) in x_axis_groups:
            # Python 2 and 3 have different rules for ordering comparisons
            # https://docs.python.org/3/whatsnew/3.0.html#ordering-comparisons
            # http://stackoverflow.com/a/3484456
            #
            # Here we're trying to sort the iterator based on values in the
            # _data attribute, which are lists of dicts, holding model data.
            #
            # When we try to render charts using sources from two different
            # models these dicts have different keys and the comparison
            # list_A < list_B fails with
            # TypeError: unorderable types: dict() < dict()
            #
            # for example try:
            # [{'a':1}, {'b':2}] < [{'a':1}, {'b':2, 'c':3}]
            #
            # This is used in demoproject.chartdemo.multi_table_same_x()!
            #
            # At the moment I don't have an idea how to solve this
            # but disabling the sort seems to work, at least in the demo!
            #
            # itr1 is fields which will be plotted on the same xAxis
            # these fields may be coming from different tables.
            # The only reason for the sort seems to be groupby below.
            # groupby() filters the unique values, which is only relevant
            # if one of the values is repeated, e.g. we want to plot the
            # same field twice in the same Chart, on the same x axis!
            # which doesn't seem to be possible !
            if self.PY2:
                itr1 = sorted(itr1, key=sort2_fn)
            for _vqs_num, (_, itr2) in enumerate(groupby(itr1, sort2_fn)):
                x_axis_vqs_groups[x_axis][_vqs_num] = _x_vqs = {}
                for tk, td in itr2:
                    _x_vqs.setdefault(td['_x_axis_term'], []).append(tk)
        return x_axis_vqs_groups

    def _set_default_hcoptions(self, chart_options):
        """Set some default options, like xAxis title, yAxis title, chart
        title, etc.
        """
        so = self.series_options
        dss = self.datasource.series
        self.hcoptions = RecursiveDefaultDict({})
        if chart_options is not None:
            self.hcoptions.update(chart_options)
        self.hcoptions['series'] = []
        # Set title
        title = ''
        for _, vqs_group in self.x_axis_vqs_groups.items():
            for _, x_y_terms in vqs_group.items():
                for x_term, y_terms in x_y_terms.items():
                    title += ', '.join([dss[y_term]['field_alias'].title()
                                        for y_term in y_terms])
                    title += ' vs. '
                    title += dss[x_term]['field_alias'].title()
                title += ' & '
        if not self.hcoptions['title']['text']:
            self.hcoptions['title']['text'] = title[:-3]
        # if xAxis and yAxis are supplied as a dict, embed it in a list
        # (needed for multiple axes)
        xAxis, yAxis = self.hcoptions['xAxis'], self.hcoptions['yAxis']
        if isinstance(xAxis, dict):
            self.hcoptions['xAxis'] = [xAxis]
        if isinstance(yAxis, dict):
            self.hcoptions['yAxis'] = [yAxis]
        # set renderTo
        if not self.hcoptions['chart']['renderTo']:
            self.hcoptions['chart']['renderTo'] = 'container'

        term_x_axis = [(dss[d['_x_axis_term']]['field_alias'].title(),
                        d.get('xAxis', 0))
                       for (k, d) in so.items()]
        term_y_axis = [(dss[k]['field_alias'].title(), d.get('xAxis', 0))
                       for (k, d) in so.items()]
        max_x_axis = max(t[1] for t in term_x_axis)
        max_y_axis = max(t[1] for t in term_y_axis)
        x_axis_len = len(self.hcoptions['xAxis'])
        y_axis_len = len(self.hcoptions['yAxis'])
        if max_x_axis >= x_axis_len:
            self.hcoptions['xAxis']\
              .extend([RecursiveDefaultDict({})]*(max_x_axis+1-x_axis_len))
        for i, x_axis in enumerate(self.hcoptions['xAxis']):
            if not x_axis['title']['text']:
                axis_title = set(t[0] for t in term_x_axis if t[1] == i)
                x_axis['title']['text'] = ' & '.join(axis_title)
        if max_x_axis == 1:
            if self.hcoptions['xAxis'][1]['opposite'] is not False:
                self.hcoptions['xAxis'][1]['opposite'] = True

        if max_y_axis >= y_axis_len:
            self.hcoptions['yAxis']\
              .extend([RecursiveDefaultDict({})]*(max_y_axis+1-y_axis_len))
        for i, y_axis in enumerate(self.hcoptions['yAxis']):
            if not y_axis['title']['text']:
                axis_title = set(t[0] for t in term_y_axis if t[1] == i)
                y_axis['title']['text'] = ' & '.join(axis_title)
        if max_y_axis == 1:
            if self.hcoptions['yAxis'][1]['opposite'] is not False:
                self.hcoptions['yAxis'][1]['opposite'] = True

    def generate_plot(self):
        # find all x's from different datasources that need to be plotted on
        # same xAxis and also find their corresponding y's
        def cht_typ_grp(y_term):
            return ('scatter' if self.series_options[y_term]['type'] in
                    ['scatter', 'pie'] else 'line')

        # reset the series
        self.hcoptions['series'] = []
        dss = self.datasource.series
        for x_axis_num, vqs_groups in self.x_axis_vqs_groups.items():
            y_hco_list = []
            try:
                x_sortf, x_mapf, x_mts = self.x_sortf_mapf_mts[x_axis_num]
            except IndexError:
                x_sortf, x_mapf, x_mts = (None, None, False)
            ptype_x_y_terms = defaultdict(list)
            for vqs_group in vqs_groups.values():
                x_term, y_terms_all = tuple(vqs_group.items())[0]
                y_terms_by_type = defaultdict(list)
                for y_term in y_terms_all:
                    y_terms_by_type[cht_typ_grp(y_term)].append(y_term)
                for y_type, y_term_list in y_terms_by_type.items():
                    ptype_x_y_terms[y_type].append((x_term, y_term_list))

            # ptype = plot type i.e. 'line', 'scatter', 'area', etc.
            for ptype, x_y_terms_tuples in ptype_x_y_terms.items():
                y_fields_multi = []
                y_aliases_multi = []
                y_types_multi = []
                y_hco_list_multi = []
                y_values_multi = OrderedDict()
                y_terms_multi = []
                for x_term, y_terms in x_y_terms_tuples:
                    # x related
                    x_vqs = dss[x_term]['_data']
                    x_field = dss[x_term]['field']
                    # y related
                    y_fields = [dss[y_term]['field'] for y_term in y_terms]
                    y_aliases = [dss[y_term]['field_alias'] for y_term
                                 in y_terms]
                    y_types = [self.series_options[y_term].get('type', 'line')
                               for y_term in y_terms]
                    y_hco_list = [RecursiveDefaultDict(
                                    copy.deepcopy(
                                        self.series_options[y_term])) for
                                  y_term in y_terms]
                    for opts, alias, typ in zip(
                                                y_hco_list,
                                                y_aliases,
                                                y_types):
                        opts.pop('_x_axis_term')
                        opts['name'] = alias
                        opts['type'] = typ
                        opts['data'] = []

                    if ptype == 'scatter' or (ptype == 'line' and
                                              len(x_y_terms_tuples) == 1):
                        if x_mts:
                            if x_mapf:
                                data = ((x_mapf(_getattr(value_obj, x_field)),
                                         [_getattr(value_obj, y_field)
                                          for y_field in y_fields])
                                        for value_obj in x_vqs)
                                sort_key = ((lambda x_y: x_sortf(x_y[0]))
                                            if x_sortf is not None else None)
                                data = sorted(data, key=sort_key)
                        else:
                            sort_key = ((lambda x_y: x_sortf(x_y[1]))
                                        if x_sortf is not None else None)
                            data = sorted(
                                    ((_getattr(value_obj, x_field),
                                     [_getattr(value_obj, y_field)
                                      for y_field in y_fields])
                                     for value_obj in x_vqs),
                                    key=sort_key)
                            if x_mapf:
                                data = [(x_mapf(x), y) for (x, y) in data]

                        if ptype == 'scatter':
                            if self.series_options[y_term]['type'] == 'scatter': # noqa
                                # scatter plot
                                for x_value, y_value_tuple in data:
                                    for opts, y_value in zip(y_hco_list,
                                                             y_value_tuple):
                                        opts['data'].append((x_value, y_value))
                                self.hcoptions['series'].extend(y_hco_list)
                            else:
                                # pie chart
                                for x_value, y_value_tuple in data:
                                    for opts, y_value in zip(y_hco_list,
                                                             y_value_tuple):
                                        opts['data'].append((unicode(x_value),
                                                             y_value))
                                self.hcoptions['series'].extend(y_hco_list)

                        if ptype == 'line' and len(x_y_terms_tuples) == 1:
                            # all other chart types - line, area, etc.
                            hco_x_axis = self.hcoptions['xAxis']
                            if len(hco_x_axis) - 1 < x_axis_num:
                                hco_x_axis.extend([RecursiveDefaultDict({})] *
                                                  (x_axis_num -
                                                   (len(hco_x_axis) -
                                                    1)))
                            hco_x_axis[x_axis_num]['categories'] = []
                            for x_value, y_value_tuple in data:
                                hco_x_axis[x_axis_num]['categories']\
                                  .append(x_value)
                                for opts, y_value in zip(y_hco_list,
                                                         y_value_tuple):
                                    opts['data'].append(y_value)
                            self.hcoptions['series'].extend(y_hco_list)
                    else:
                        data = ((_getattr(value_obj, x_field),
                                 [_getattr(value_obj, y_field) for y_field in
                                  y_fields])
                                for value_obj in x_vqs)

                        y_terms_multi.extend(y_terms)
                        y_fields_multi.extend(y_fields)
                        y_aliases_multi.extend(y_aliases)
                        y_types_multi.extend(y_types)
                        y_hco_list_multi.extend(y_hco_list)

                        len_y_terms_multi = len(y_terms_multi)
                        ext_len = len(y_terms_multi) - len(y_terms)
                        for x_value, y_value_tuple in data:
                            try:
                                cur_y = y_values_multi[x_value]
                                cur_y.extend(y_value_tuple)
                            except KeyError:
                                y_values_multi[x_value] = [None]*ext_len
                                y_values_multi[x_value].extend(y_value_tuple)
                        for _y_vals in y_values_multi.values():
                            if len(_y_vals) != len_y_terms_multi:
                                _y_vals.extend([None]*len(y_terms))
                if y_terms_multi:
                    hco_x_axis = self.hcoptions['xAxis']
                    if len(hco_x_axis) - 1 < x_axis_num:
                        hco_x_axis.extend([RecursiveDefaultDict({})] *
                                          (x_axis_num - (len(hco_x_axis)-1)))
                    hco_x_axis[x_axis_num]['categories'] = []

                    if x_mts:
                        if x_mapf:
                            data = ((x_mapf(x_value), y_vals) for
                                    (x_value, y_vals) in
                                    y_values_multi.items())
                            sort_key = ((lambda x_y: x_sortf(x_y[1]))
                                        if x_sortf is not None
                                        else None)
                            data = sorted(data, key=sort_key)
                    else:
                        data = y_values_multi.items()
                        sort_key = ((lambda x_y: x_sortf(x_y[1])) if x_sortf
                                    is not None else None)
                        data = sorted(data, key=sort_key)
                        if x_mapf:
                            data = [(x_mapf(x), y) for (x, y) in data]

                    for x_value, y_vals in data:
                        hco_x_axis[x_axis_num]['categories']\
                          .append(x_value)
                        for opts, y_value in zip(y_hco_list_multi, y_vals):
                            opts['data'].append(y_value)
                    self.hcoptions['series'].extend(y_hco_list_multi)


class PivotChart(BaseChart):

    def __init__(self, datasource, series_options, chart_options=None):
        """Creates the PivotChart object.

        **Arguments**:

        - **datasource** (**required**) - a ``PivotDataPool`` object that
          holds the terms and other information to plot the chart from.

        - **series_options** (**required**) - specifies the options to plot
          the terms on the chart. It is of the form ::

            [{'options': {
                #any items from HighChart series. For ex.
                'type': 'column'
                },
              'terms': [
                'a_valid_term',
                'other_valid_term': {
                  #any options to override. For ex.
                 'type': 'area',
                  ...
                  },
                ...
                ]
              },
              ... #repeat dicts with 'options' & 'terms'
              ]

          Where -

          - **options** (**required**) - a ``dict``. Any of the parameters
            from the `Highcharts options object - series array
            <http://www.highcharts.com/ref/#series>`_ are valid as entries in
            the ``options`` dict except ``data`` (because data array is
            generated from your datasource by chartit). For example, ``type``,
            ``xAxis``, etc. are all valid entries here.

            .. note:: The items supplied in the options dict are not validated
               to make sure that Highcharts actually supports them. Any
               invalid options are just passed to Highcharts JS which silently
               ignores them.

          - **terms** (**required**) - a ``list``. Only terms that are present
            in the corresponding datasource are valid.

            .. note:: All the ``terms`` are plotted on the ``y-axis``. The
              **categories of the datasource are plotted on the x-axis. There
              is no option to override this.**

            Each of the ``terms`` must either be a ``str`` or a ``dict``. If
            entries are dicts, the keys need to be valid terms and the values
            need to be any options to override the default options. For
            example, ::

              [{'options': {
                  'type': 'column',
                  'yAxis': 0},
                'terms': [
                  'temperature',
                  {'rainfall': {
                      'type': 'line',
                      'yAxis': 1}}]}]

            plots a pivot column chart of temperature on yAxis: 0 and a line
            pivot chart of rainfall on yAxis: 1. This can alternatively be
            expressed as two separate entries: ::

              [{'options': {
                  'type': 'column',
                  'yAxis': 0},
                'terms': [
                    'temperature']},
               {'options': {
                  'type': 'line',
                  'yAxis': 1},
                'terms': [
                    'rainfall']}]

        - **chart_options** (*optional*) - a ``dict``. Any of the options from
          the `Highcharts options object <http://www.highcharts.com/ref/>`_
          are valid (except the options in the ``series`` array which are
          passed in the ``series_options`` argument. The following
          ``chart_options`` for example, set the chart title and the axes
          titles. ::

              {'chart': {
                 'title': {
                   'text': 'Weather Chart'}},
               'xAxis': {
                 'title': 'month'},
               'yAxis': {
                 'title': 'temperature'}}

          .. note:: The items supplied in the ``chart_options`` dict are not
             validated to make sure that Highcharts actually supports them.
             Any invalid options are just passed to Highcharts JS which
             silently ignores them.

        **Raises**:

        - ``APIInputError`` if any of the terms are not present in the
          corresponding datasource or if the ``series_options`` cannot be
          parsed.
        """
        warnings.warn('PivotChart will be deprecated soon. Use Chart instead!',
                      DeprecationWarning)
        super(PivotChart, self).__init__()
        if not isinstance(datasource, PivotDataPool):
            raise APIInputError("%s must be an instance of PivotDataPool." %
                                datasource)
        self.datasource = datasource
        self.series_options = clean_pcso(series_options, self.datasource)
        if chart_options is None:
            chart_options = RecursiveDefaultDict({})
        self.set_default_hcoptions()
        self.hcoptions.update(chart_options)
        # Now generate the plot
        self.generate_plot()

    def set_default_hcoptions(self):
        self.hcoptions = RecursiveDefaultDict({})
        # series and terms
        dss = self.datasource.series
        terms = list(self.series_options.keys())
        # legend by
        lgby_dict = dict(((t, dss[t]['legend_by']) for t in terms))
        lgby_vname_lists = [[dss[t]['field_aliases'].get(lgby, lgby)
                            for lgby in lgby_tuple]
                            for (t, lgby_tuple) in lgby_dict.items()]
        lgby_titles = (':'.join(lgby_vname_list).title() for
                       lgby_vname_list in lgby_vname_lists)
        # chart title
        term_titles = (t.title() for t in terms)
        title = ''
        for t, lg in zip(term_titles, lgby_titles):
            if not lg:
                title += "%s, " % t
            else:
                title += "%s (lgnd. by %s), " % (t, lg)
        categories = dss[terms[0]]['categories']
        categories_vnames = [dss[terms[0]]['field_aliases'][c].title()
                             for c in categories]
        category_title = ':'.join(categories_vnames)
        chart_title = "%s vs. %s" % (title[:-2], category_title)
        self.hcoptions['title']['text'] = chart_title

    def generate_plot(self):
        cv_raw = self.datasource.cv_raw
        hco_series = []
        for term, options in self.series_options.items():
            dss = self.datasource.series
            for lv in dss[term]['_lv_set']:
                data = [dss[term]['_cv_lv_dfv'][cv].get(lv, None) for cv
                        in cv_raw]
                term_pretty_name = term.replace('_', ' ')
                name = term_pretty_name.title() if not lv else "-".join(lv)
                hco = copy.deepcopy(options)
                hco['data'] = data
                hco['name'] = name
                hco_series.append(hco)
        self.hcoptions['series'] = hco_series
        self.hcoptions['xAxis']['categories'] = [':'.join(cv) for cv in
                                                 self.datasource.cv]
