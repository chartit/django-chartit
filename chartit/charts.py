import copy
from collections import defaultdict
from itertools import groupby, izip
# use SortedDict instead of native OrderedDict for Python 2.6 compatibility
from django.utils.datastructures import SortedDict

from highcharts import HCOptions
from validation import clean_pcso, clean_cso, clean_x_sortf_mapf_mts
from exceptions import APIInputError
from chartdata import PivotDataPool, DataPool

class Chart(object):
    
    def __init__(self, datasource, series_options, chart_options=None,
                 x_sortf_mapf_mts=None):
        self.user_input = locals()
        if not isinstance(datasource, DataPool):
            raise APIInputError("%s must be an instance of DataPool." 
                                %datasource)
        self.datasource = datasource
        self.series_options = clean_cso(series_options, self.datasource)
        self.x_sortf_mapf_mts = clean_x_sortf_mapf_mts(x_sortf_mapf_mts)
        self.x_axis_vqs_groups = self._groupby_x_axis_and_vqs()
        self._set_default_hcoptions(chart_options)
        self.generate_plot()
    
    def _groupby_x_axis_and_vqs(self):
        """Returns a list of list of lists where each list has the term and 
        option dict with the same xAxis and within each list with same xAxis,
        all items in same sub-list have items with same ValueQuerySet.
        
        Here is an example of what this function would return. ::
        
        [
         [[(term-1-A-1, opts-1-A-1), (term-1-A-2, opts-1-A-2), ...],
          [(term-1-B-1, opts-1-B-1), (term-1-B-2, opts-1-B-2), ...],
          ...],
         [[term-2-A-1, opts-2-A-1), (term-2-A-2, opts-2-A-2), ...],
          [term-2-B-2, opts-2-B-2), (term-2-B-2, opts-2-B-2), ...],
          ...],
          ...
          ]
          
        In the above example,
        
        - term-1-*-* all have same xAxis.
        - term-*-A-* all are from same ValueQuerySet (table)
        """
        dss = self.datasource.series
        x_axis_vqs_groups = defaultdict(dict)
        sort_fn = lambda (tk, td): td.get('xAxis', 0)
        so = sorted(self.series_options.items(), key=sort_fn)
        x_axis_groups = groupby(so, sort_fn)
        for (x_axis, itr1) in x_axis_groups:
            sort_fn = lambda (tk, td): dss[td['_x_axis_term']]['_data']
            itr1 = sorted(itr1, key=sort_fn)
            for _vqs_num, (_data, itr2) in enumerate(groupby(itr1, sort_fn)):
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
        self.hcoptions = HCOptions({})
        if chart_options is not None:
            self.hcoptions.update(chart_options)
        self.hcoptions['series'] = []
        # Set title
        title = ''
        for x_axis_num, vqs_group in self.x_axis_vqs_groups.items():
            for vqs_num, x_y_terms in  vqs_group.items():
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
              .extend([HCOptions({})]*(max_x_axis+1-x_axis_len))
        for i, x_axis in enumerate(self.hcoptions['xAxis']):
            if not x_axis['title']['text']:
                axis_title = set(t[0] for t in term_x_axis if t[1] == i)
                x_axis['title']['text'] = ' & '.join(axis_title)
        if max_x_axis == 1:
            if self.hcoptions['xAxis'][1]['opposite'] != False:
                self.hcoptions['xAxis'][1]['opposite'] = True
                
        if max_y_axis >= y_axis_len:
            self.hcoptions['yAxis']\
              .extend([HCOptions({})]*(max_y_axis+1-y_axis_len))
        for i, y_axis in enumerate(self.hcoptions['yAxis']):
            if not y_axis['title']['text']:
                axis_title = set(t[0] for t in term_y_axis if t[1] == i)
                y_axis['title']['text'] = ' & '.join(axis_title)
        if max_y_axis == 1:
            if self.hcoptions['yAxis'][1]['opposite'] != False:
                self.hcoptions['yAxis'][1]['opposite'] = True
    
    def generate_plot(self):
        # reset the series
        self.hcoptions['series'] = []
        dss = self.datasource.series
        # find all x's from different datasources that need to be plotted on 
        # same xAxis and also find their corresponding y's
        cht_typ_grp = lambda y_term: ('scatter' if 
                                      self.series_options[y_term]['type'] 
                                      in ['scatter', 'pie'] else 'line')
        for x_axis_num, vqs_groups in self.x_axis_vqs_groups.items():
            y_hco_list = []
            try:
                x_sortf, x_mapf, x_mts = self.x_sortf_mapf_mts[x_axis_num]
            except IndexError:
                x_sortf, x_mapf, x_mts = (None, None, False)
            ptype_x_y_terms = defaultdict(list)
            for vqs_group in vqs_groups.values(): 
                x_term, y_terms_all = vqs_group.items()[0]
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
                y_values_multi = SortedDict()
                y_terms_multi = []
                for x_term, y_terms in x_y_terms_tuples:
                    # x related
                    x_vqs = dss[x_term]['_data']
                    x_field = dss[x_term]['field']
                    # y related 
                    y_fields = [dss[y_term]['field'] for y_term in y_terms]
                    y_aliases = [dss[y_term]['field_alias'] for y_term 
                                 in y_terms]
                    y_types = [self.series_options[y_term].get('type','line') 
                               for y_term in y_terms]
                    y_hco_list = [HCOptions(
                                    copy.deepcopy(
                                        self.series_options[y_term])) for 
                                  y_term in y_terms]
                    for opts, alias, typ in zip(y_hco_list,y_aliases,y_types):
                        opts.pop('_x_axis_term')
                        opts['name'] = alias
                        opts['type'] = typ
                        opts['data'] = []
                    
                    if ptype == 'scatter' or (ptype == 'line' and 
                                              len(x_y_terms_tuples) == 1):
                        if x_mts:
                            if x_mapf: 
                                data = ((x_mapf(value_dict[x_field]), 
                                         [value_dict[y_field] for y_field 
                                          in y_fields]) 
                                        for value_dict in x_vqs)
                                sort_key = ((lambda(x, y): x_sortf(x)) 
                                            if x_sortf is not None else None)
                                data = sorted(data, key=sort_key)
                        else:
                            sort_key = ((lambda(x, y): x_sortf(x)) 
                                            if x_sortf is not None else None)
                            data = sorted(
                                    ((value_dict[x_field], 
                                     [value_dict[y_field] for y_field in 
                                      y_fields]) 
                                     for value_dict in x_vqs), 
                                    key=sort_key)
                            if x_mapf:
                                data = [(x_mapf(x), y) for (x, y) in data]
                            
                        if ptype == 'scatter':
                            #scatter plot and pie chart
                            for x_value, y_value_tuple in data:
                                for opts, y_value in izip(y_hco_list,
                                                          y_value_tuple):
                                    opts['data'].append((x_value, y_value))
                            self.hcoptions['series'].extend(y_hco_list)
                            
                        if ptype == 'line' and len(x_y_terms_tuples) == 1:
                            # all other chart types - line, area, etc.
                            hco_x_axis = self.hcoptions['xAxis']
                            if len(hco_x_axis) - 1 < x_axis_num:
                                    hco_x_axis.extend([HCOptions({})]*
                                                      (x_axis_num - 
                                                       (len(hco_x_axis) - 
                                                        1)))
                            hco_x_axis[x_axis_num]['categories'] = []
                            for x_value, y_value_tuple in data:
                                hco_x_axis[x_axis_num]['categories']\
                                  .append(x_value)
                                for opts, y_value in izip(y_hco_list, 
                                                          y_value_tuple):
                                    opts['data'].append(y_value)
                            self.hcoptions['series'].extend(y_hco_list)
                    else:
                        data = ((value_dict[x_field],
                                 [value_dict[y_field] for y_field in 
                                  y_fields])
                                for value_dict in x_vqs)
                        
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
                                y_values_multi[x_value]\
                                  .extend(y_value_tuple)
                        for _y_vals in y_values_multi.values():
                            if len(_y_vals) != len_y_terms_multi:
                                _y_vals.extend([None]*len(y_terms))
                if y_terms_multi:
                    hco_x_axis = self.hcoptions['xAxis']
                    if len(hco_x_axis) - 1 < x_axis_num:
                            hco_x_axis\
                              .extend([HCOptions({})]*
                                      (x_axis_num - (len(hco_x_axis)-1)))
                    hco_x_axis[x_axis_num]['categories'] = []
                    
                    if x_mts:
                        if x_mapf: 
                            data = ((x_mapf(x_value), y_vals) for 
                                    (x_value, y_vals) in 
                                    y_values_multi.iteritems())
                            sort_key = ((lambda(x, y): x_sortf(x)) if x_sortf 
                                        is not None else None)
                            data = sorted(data, key=sort_key)
                    else:
                        data = y_values_multi.iteritems()
                        sort_key = ((lambda(x, y): x_sortf(x)) if x_sortf 
                                    is not None else None)
                        data = sorted(data, key=sort_key)
                        if x_mapf:
                            data = [(x_mapf(x), y) for (x, y) in data]
                    
                    for x_value, y_vals in data:
                        hco_x_axis[x_axis_num]['categories']\
                          .append(x_value)
                        for opts, y_value in izip(y_hco_list_multi, y_vals):
                            opts['data'].append(y_value)
                    self.hcoptions['series'].extend(y_hco_list_multi)
                    
                    
class PivotChart(object):
    
    def __init__(self, datasource, series_options, chart_options=None):
        self.user_input = locals()
        if not isinstance(datasource, PivotDataPool):
            raise APIInputError("%s must be an instance of PivotDataPool." 
                                %datasource)
        self.datasource = datasource
        self.series_options = clean_pcso(series_options, self.datasource)
        self.set_default_hcoptions()
        self.hcoptions.update(chart_options)
        # Now generate the plot
        self.generate_plot()
    
    def set_default_hcoptions(self):
        self.hcoptions = HCOptions({})
        # series and terms
        dss = self.datasource.series
        terms = self.series_options.keys()
        # legend by
        lgby_dict = dict(((t, dss[t]['legend_by']) for t in terms))
        lgby_vname_lists= [[dss[t]['field_aliases'].get(lgby, lgby) 
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
                title += "%s (lgnd. by %s), "  %(t, lg)
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
                #name = '-'.join(dstd['legend_by']) + ":" + "-".join(lv)
                term_pretty_name = term.replace('_', ' ')
                name = term_pretty_name.title() if not lv else "-".join(lv) 
                hco = copy.deepcopy(options)
                hco['data'] = data
                hco['name'] = name
                hco_series.append(hco)
        self.hcoptions['series'] = hco_series
        self.hcoptions['xAxis']['categories'] = [':'.join(cv) for cv in 
                                                 self.datasource.cv]

