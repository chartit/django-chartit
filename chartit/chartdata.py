import copy
from collections import defaultdict
from itertools import groupby, chain, islice
from operator import itemgetter
# use SortedDict instead of native OrderedDict for Python 2.6 compatibility
from django.utils.datastructures import SortedDict
from validation import clean_dps, clean_pdps
from chartit.validation import clean_sortf_mapf_mts

class DataPool(object):
    """DataPool holds the data retrieved from various models (tables)."""
    
    def __init__(self, series):
        """Create a DataPool object as specified by the ``series``.
        
        :Arguments: 
        
        - **series** *(list of dict)* - specifies the what data to retrieve 
          and where to retrieve it from. It is of the form ::
          
            [{'options': {
               'source': a django model, Manager or QuerySet,
               },
             'terms': [
               'a_valid_field_name', ... ,
               {'any_name': 'a_valid_field_name', ... },
               ]
            },
            ... 
            ]
        
          Where 
          
          - **options** - is a dict with one key.
          
            + **source** - is either a ``Model``, ``Manager`` or a 
              ``QuerySet``.
              
          - **terms** - is a list. Each element in ``terms`` is either 
            
            1. a ``str`` - needs to be a valid model field for the 
               corresponding ``source``, or 
            2. a ``dict`` - need to be of the form 
               ``{'any_name': 'a_valid_field_name', ...}``. 
          
          To retrieve data from multiple models or QuerySets, just add more 
          dictionaries with the corresponding ``options`` and terms.
          
        :Raises:
          
        - **APIInputError** - sif the ``series`` argument has any invalid 
          parameters.
        
         
        .. warning:: All elements in ``terms`` **must be unique** across all 
           the dictionaries in the ``series`` list. If there are two terms 
           with same ``name``, the latter one is going to overwrite the one 
           before it.
        
        For example, the following is **wrong**: ::
        
          [{'options': {
              'source': SomeModel},
            'terms':[
              'foo', 
              'bar']},
           {'options': {
              'source': OtherModel},
            'terms':[
              'foo']}]
              
        In this case, the term ``foo`` from ``OtherModel`` is going to 
        **overwrite** ``foo`` from ``SomeModel``. 
        
        Here is the **right** way of retrieving data from two different models 
        both of which have the same field name. ::
        
          [{'options': {
             'source': SomeModel},
            'terms':[
              'foo', 
              'bar']},
           {'options': {
             'source': OtherModel},
            'terms':[
              {'foo_2': 'foo'}]}]
         """
        # Save user input to a separate dict. Can be used for debugging.
        self.user_input = {}
        self.user_input['series'] = copy.deepcopy(series)
        self.series = clean_dps(series)
        self.query_groups = self._group_terms_by_query()
        # Now get data
        self._get_data()
    
    def _group_terms_by_query(self, sort_by_term=None, *addl_grp_terms):
        """Groups all the terms that can be extracted in a single query. This 
        reduces the number of database calls. 
        
        :returns: 
        
        - a list of sub-lists where each sub-list has items that can 
          all be retrieved with the same query (i.e. terms from the same source 
          and any additional criteria as specified in addl_grp_terms).
        """
        # TODO: using str(source.query) was the only way that I could think of
        # to compare whether two sources are exactly same. Need to figure out
        # if there is a better way. - PG
        sort_grp_fn = lambda (tk, td): tuple(chain(str(td['source'].query), 
                                              [td[t] for t in addl_grp_terms]))
        s = sorted(self.series.items(), key=sort_grp_fn)
        # The following groupby will create an iterator which returns 
        # <(grp-1, <(tk, td), ...>), (grp-2, <(tk, td), ...>), ...>
        # where sclt is a source, category, legend_by tuple
        qg = groupby(s, sort_grp_fn)
        if sort_by_term is not None:
            sort_by_fn = lambda (tk, td): -1*(abs(td[sort_by_term]))
        else:
            sort_by_fn = None
        qg = [sorted(itr, key=sort_by_fn) for (grp, itr) in qg]
        return qg

    def _generate_vqs(self):
        # query_groups is a list of lists.
        for tk_td_tuples in self.query_groups:
            src = tk_td_tuples[0][1]['source']
            vqs = src.values(*(td['field'] for (tk, td) in tk_td_tuples))
            yield tk_td_tuples, vqs
    
    def _get_data(self):
        for tk_td_tuples, vqs in self._generate_vqs():
            vqs_list = list(vqs)
            for tk, td in tk_td_tuples:
                # everything has a reference to the same list
                self.series[tk]['_data'] = vqs_list

class PivotDataPool(DataPool):
    """PivotDataPool holds the data retrieved from various tables (models) and 
    then *pivoted* against the category fields."""
    
    def __init__(self, series, top_n_term=None, top_n=None, pareto_term=None, 
                 sortf_mapf_mts=None):
        """ Creates a PivotDataPool object. 
        
        :Arguments: 
        
        - **series** (**required**) - a list of dicts that specifies the what 
          data to retrieve, where to retrieve it from and how to pivot the 
          data. It is of the form ::
           
            [{'options': {
                'source': django Model, Manager or QuerySet ,
                'categories': ['a_valid_field', ...],
                'legend_by': ['a_valid_field', ...] (optional),
                'top_n_per_cat': a number (optional),
              },
              'terms': {
                'any_name_here': django Aggregate,
                'some_other_name':{
                  'func': django Aggregate,
                  #any options to override
                  ...
                },
              ...
              }
             },
             ... #repeat dicts with 'options' & 'terms'
            ]
        
          Where 
        
          - **options** - is a dict that specifies the common options for all 
            the terms. 
            
            + **source** (**required**) - is either a ``Model``, ``Manager`` 
              or a ``QuerySet``.
            + **categories** (**required**) - is a list of model fields by 
              which the data needs to be pivoted by. If there is only a single 
              item, ``categories`` can just be a string instead of a list with 
              single element.  
              
              For example if you have a model with ``country``, ``state``, 
              ``county``, ``city``, ``date``, ``rainfall``, ``temperature`` 
              and you want to pivot the data by ``country`` and ``state``, 
              then ``categories = ['country', 'state']`` .
              
              .. note:: Order of elements in the ``categories`` list matters!
              
              ``categories = ['country', 'state']`` groups your data first by 
              ``country`` and then by ``state`` when running the SQL query. 
              This obviously is not the same as grouping by ``state`` first 
              and then by ``country``.
                  
            + **legend_by** (*optional*) - is a list of model fields by which 
              the data needs to be legended by. For example, in the above case, 
              if you want to legend by ``county`` and ``city``, then 
              ``legend_by = ['county', 'city']``
              
              .. note:: Order of elements in the ``legend_by`` list matters!
              
              See the note in ``categories`` above.
              
            + **top_n_per_cat** (*optional*) - The number of top items that 
              the legended entries need to be limited to in each category. For 
              example, in the above case, if you wanted only the top 3 
              ``county/cities`` with highest rainfall for each of the 
              ``country/state``, then ``top_n_per_cat = 3``.
            
          - **terms** - is a ``dict``. The keys can be any strings (but helps 
            if they are meaningful aliases for the field). The values can 
            either be  
          
            + a django ``Aggregate`` : of a valid field in corresponding model. 
              For example, ``Avg('temperature')``, ``Sum('price')``, etc. or 
            + a ``dict``: In this case the ``func`` must specify relevant 
              django aggregate to retrieve. For example 
              ``'func': Avg('price')``. The dict can also have any additional 
              entries from the options dict. Any entries here will override 
              the entries in the ``options`` dict.
        
        - **top_n_term** (*optional*) - a string. Must be one of the keys in 
          the corresponding ``terms`` in the ``series`` argument.
         
        - **top_n** (*optional*) - an integer. The number of items for the 
          corresponding ``top_n_term`` that need to be retained. 
         
          If ``top_n_term`` and ``top_n`` are present, only the ``top_n`` number 
          of items are going to displayed in the pivot chart. For example, if 
          you want to plot only the top 5 states with highest average rainfall, 
          you can do something like this. ::
            
            PivotDataPool(
              series = [
                 {'options': {
                    'source': RainfallData.objects.all(),
                    'categories': 'state'},
                  'terms': { 
                    'avg_rain': Avg('rainfall')}}],
              top_n_term = 'avg_rain',
              top_n = 5)
          
          Note that the ``top_n_term`` is ``'avg_rain'`` and **not** ``state`` ; 
          because we want to limit by the average rainfall.
        
        - **pareto_term** (*optional*) - the term with respect to which the 
          pivot chart needs to be paretoed by. 
          
          For example, if you want to plot the average rainfall on the y-axis 
          w.r.t the state on the x-axis and want to pareto by the average 
          rainfall, you can do something like this. ::
          
            PivotDataPool(
              series = [
                 {'options': {
                    'source': RainfallData.objects.all(),
                    'categories': 'state'},
                  'terms': { 
                    'avg_rain': Avg('rainfall')}}],
              pareto_term = 'avg_rain')
                
        - **sortf_mapf_mts** (*optional*) - a ``tuple`` with three elements of
          the form ``(sortf, mapf, mts)`` where 
          
          + **sortf** - is a function (or a callable) that is used as a `key`
            when sorting the category values. 
             
            For example, if ``categories = 'month_num'`` and if the months
            need to be sorted in reverse order, then ``sortf`` can be :: 
              
              sortf = lambda *x: (-1*x[0],) 
          
            .. note:: ``sortf`` is passed the category values as tuples and 
               must return tuples! 
              
            If ``categories`` is ``['city', 'state']`` and if the category 
            values returned need to be sorted with state first and then city, 
            then ``sortf`` can be :: 
              
              sortf = lambda *x: (x[1], x[0])
              
            The above ``sortf`` is passed tuples like 
            ``('San Francisco', 'CA')``, ``('New York', 'NY')``, ``...`` and 
            it returns tuples like ``('CA', 'San Francisco')``, 
            ``('NY', 'New York')``, ``...`` which when used as keys to sort the 
            category values will obviously first sort by state and then by 
            city.
                  
          + **mapf** - is a function (or a callable) that defines how the 
            category values need to be mapped.
            
            For example, let's say ``categories`` is ``'month_num'`` and that 
            the category values that are retrieved from your database are 
            ``1``, ``2``, ``3``, etc. If you want month *names* as the 
            category values instead of month numbers, you can define a 
            ``mapf`` to transform the month numbers to month names like so ::
              
              def month_name(*t):
                  names ={1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 
                          5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 
                          9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
                  month_num = t[0]
                  return (names[month_num], )
              
              mapf = month_name
            
            .. note:: ``mapf`` like ``sortf`` is passed the category values 
               as tuples and must return tuples.
               
          + **mts** - *map then sort* ; a ``bool``. If ``True``, the 
            category values are mapped first and then sorted, and if 
            ``False`` category values are sorted first and then mapped.
            
            In the above example of month names, we ``mts`` must be ``False``
            because the months must first be sorted based on their number 
            and then mapped to their names. If ``mts`` is ``True``, the 
            month numbers would be transformed to the month names, and then 
            sorted, which would yield an order like ``Apr``, ``Aug``, 
            ``Dec``, etc. (not what we want).
        
        :Raises:    
          
        - **APIInputError** - if the ``series`` argument has any invalid 
          parameters.

        Here is a full example of a ``series`` term that retrieves the 
        average temperature of the top 3 cities in each country/state and 
        the average rainfall of the top 2 cities in each country/state. ::
        
          [{'options': {
              'source': Weather.objects.all(),
              'categories': ['country', 'state'],
              'legend_by': 'city', 
              'top_n_per_cat': 3}, 
            'terms': {
              'avg_temp': Avg('temperature'),
              'avg_rain': {
                'func': Avg('rainfall'),
                'top_n_per_cat': 2}}}]
        
        The ``'top_n_per_cat': 2`` term in ``avg_rain`` dict overrides 
        ``'top_n_per_cat': 5`` from the comon options dict. Effectively, 
        the above ``series`` retrieves the *top 2*  ``cities`` with 
        highest ``avg_rain`` in each ``country/state`` and *top 3* ``cities`` 
        with highest ``avg_temp`` in each ``country/state``.
             
        A single ``PivotDataPool`` can hold data from multiple Models. 
        If there are more models or QuerySets to retrieve the data from, 
        just add more dicts to the series list with different ``source`` 
        values.
        
        .. warning:: The ``keys`` for the ``terms`` must be **unique across 
           all the dictionaries** in the ``series`` list! If there are 
           multiple terms with same ``key``, the latter ones will just 
           overwrite the previous ones.
        
        For instance, the following example is **wrong**. ::
        
          [{'options': {
              'source': EuropeWeather.objects.all(),
              'categories': ['country', 'state']}, 
            'terms': {
              'avg_temp': Avg('temperature')}},
           {'options': {
               'source': AsiaWeather.objects.all(),
               'categories': ['country', 'state']},
            'terms': {
              'avg_temp': Avg('temperature')}}]
        
        The second ``avg_temp`` will overwrite the first one. Instead just 
        use different names for each of the keys in all the dictionaries. 
        Here is the **right** format. ::
          
          [{'options': {
              'source': EuropeWeather.objects.all(),
              'categories': ['country', 'state']}, 
            'terms': {
              'europe_avg_temp': Avg('temperature')}},
           {'options': {
               'source': AsiaWeather.objects.all(),
               'categories': ['country', 'state']},
            'terms': {
              'asia_avg_temp': Avg('temperature')}}]
        """
        # Save user input to a separate dict. Can be used for debugging.
        self.user_input = locals()
        self.user_input['series'] = copy.deepcopy(series)
        
        self.series = clean_pdps(series)
        self.top_n_term = (top_n_term if top_n_term 
                           in self.series.keys() else None)
        self.top_n = (top_n if (self.top_n_term is not None 
                                and isinstance(top_n, int)) else 0)   
        self.pareto_term = (pareto_term if pareto_term in 
                            self.series.keys() else None)
        self.sortf, self.mapf, self.mts = clean_sortf_mapf_mts(sortf_mapf_mts)
        # query groups and data
        self.query_groups = \
          self._group_terms_by_query('top_n_per_cat','categories','legend_by')
        self._get_data()

    def _generate_vqs(self):
        """Generates and yields the value query set for each query in the  
        query group."""
        # query_groups is a list of lists.
        for tk_td_tuples in self.query_groups:
            # tk: term key, td: term dict
            # All (tk, td) tuples within the list tk_td_tuples, share the same 
            # source, categories and legend_by. So we can extract these three 
            # from the first tuple in the list.
            tk, td = tk_td_tuples[0]
            qs = td['source']
            categories = td['categories']
            legend_by = td['legend_by']
            #vqs = values queryset
            values_terms = chain(categories, legend_by)
            vqs = qs.values(*values_terms)
            # NOTE: Order of annotation is important!!!
            # So need an SortedDict. Can't use a regular dict.
            ann_terms = SortedDict((k, d['func']) for k, d in tk_td_tuples)
            vqs = vqs.annotate(**ann_terms)
            # Now order by
            top_n_per_cat = td['top_n_per_cat']
            if top_n_per_cat > 0:
                order_by = ('-' + tk,)
            elif top_n_per_cat < 0:
                order_by = (tk,)
            else:
                order_by = ()
            order_by_terms = chain(categories, order_by)
            vqs = vqs.order_by(*order_by_terms)
            yield tk_td_tuples, vqs

    def _get_data(self):
        # These are some of the attributes that will used to store some
        # temporarily generated data.
        self.cv_raw = set([])
        _pareto_by_cv = defaultdict(int)
        _cum_dfv_by_cv = defaultdict(int)
        for tk_td_tuples, vqs in self._generate_vqs():
            # tk: term key, td: term dict
            # All (tk, td) tuples within the list tk_td_tuples, share the same 
            # source, categories and legend_by. So we can extract these three 
            # from the first tuple in the list.
            tk, td = tk_td_tuples[0]
            categories = td['categories']
            legend_by = td['legend_by']
            for i, (tk, td) in enumerate(tk_td_tuples):
                # cv_lv_dfv: dict with category value, legend value as keys 
                # and datafunc-values as values.
                # For example, if
                # category = ['continent'], legend_by = ['country'] and
                # func = Sum('population_millions')
                # cv_lv_dfv = {'Asia': {'India': 1001, 'China': 1300},
                #              'Europe': {'UK': 61.8, 'France': 62.6},
                #              ... }
                cv_lv_dfv = defaultdict(dict)
                # lv_set is the set of legend_values
                # For instance, lv_set for the above example is
                # set(['India', 'China', 'UK', 'France'])
                lv_set = set()
                # cv: category value. For example, 
                # if categories = ('continent', 'country'), then
                # cv = ('NA', 'USA'), ('Asia', 'India'), etc.
                # g_vqs_by_cv = grouped ValueQuerySet (grouped by cv)
                # i.e. grouped by ('NA', 'USA'), ('Asia', 'India'), etc.
                #
                # vqs is a list of dicts. For example
                # [{'continent': 'NA', 'country': 'USA', 'pop__sum': 300}]
                for cv, g_vqs_by_cv in groupby(vqs, itemgetter(*categories)):
                    if not isinstance(cv, tuple):
                        cv = (cv,)
                    cv = tuple(map(str, cv))
                    self.cv_raw |= set([cv])
                    # For the first loop (i==0), the queryset is already 
                    # pre-sorted by value of the data func alias (for example 
                    # pop__sum) when retrieved from the DB. So don't
                    # sort it again. If we need to retrieve all the 
                    # elements (not just top n) per category 
                    # (fd['top_n_per_group'] == 0), we don't care about the 
                    # sort order. Don't sort in this case.
                    if i != 0 and td['top_n_per_cat'] != 0:
                        g_vqs_by_cv.sort(key=itemgetter(tk), 
                                         reverse=(td['top_n_per_cat']> 0))
                    # g_vqs_by_cv_dfv: Grouped Value QuerySet (grouped by 
                    # category and then by datafunc value.
                    # alias = 'population__sum'
                    # itemgetter('pop__sum') = 10 etc.
                    # So grouped by pop__sum = 10, 9, etc.
                    # NOTE: Need this step to make sure we retain duplicates 
                    # in the top n if there are multiple entries. For example
                    # if pop__sum is 10, 10, 9, 9, 7, 3, 2, 1 and we want
                    # top 3, then the result should we 10, 10, 9, 9, 7 and 
                    # not just 10, 10, 9. A simple list slice will only retain
                    # 10, 10, 9. So it is not useful. An alternative is to 
                    # group_by and then slice.
                    g_vqs_by_cv_dfv = groupby(g_vqs_by_cv,itemgetter(tk))
                    # Now that this is grouped by datafunc value, slice off
                    # if we only need the top few per each category
                    if td['top_n_per_cat'] != 0:
                        g_vqs_by_cv_dfv = islice(g_vqs_by_cv_dfv,0, 
                                               abs(td['top_n_per_cat']))
                    # Now build the result dictionary
                    # dfv = datafunc value
                    # vqs_by_c_dfv =  ValuesQuerySet by cat. and datafunc value
                    for dfv, vqs_by_cv_dfv in g_vqs_by_cv_dfv:
                        if tk == self.top_n_term:
                            _cum_dfv_by_cv[cv] += dfv
                        if tk == self.pareto_term:
                            _pareto_by_cv[cv] += dfv
                        for vd in vqs_by_cv_dfv:
                            # vd: values dict
                            # vd: {'continent': 'NA', 'country': 'USA', 
                            #      'year': 2010, 'quarter': 2,
                            #      'population__avg': 301,
                            #      'gdp__avg': 14.12}
                            # category = ('continent', 'country',)
                            # legend = ('year', 'quarter')
                            # lv = (2010, 2)
                            # dfa = 'price__max'
                            # cv_lv_dfv[('NA', 'USA')][(2010, 2)] = 301
                            try:
                                lv = itemgetter(*legend_by)(vd)
                                if not isinstance(lv, tuple):
                                    lv = (lv,)
                                lv = tuple(map(str, lv))
                            # If there is nothing to legend by i.e. 
                            # legend_by=() then itemgetter raises a TypeError. 
                            # Handle it.
                            except TypeError:
                                lv = ()
                            cv_lv_dfv[cv][lv] = vd[tk]
                            lv_set |= set([lv])
                td['_cv_lv_dfv'] = cv_lv_dfv
                td['_lv_set'] = lv_set
        # If we only need top n items, remove the other items from self.cv_raw
        if self.top_n_term:
            cum_cv_dfv_items = sorted(_cum_dfv_by_cv.items(), 
                                      key = itemgetter(1),
                                      reverse = self.top_n > 0)
            cv_dfv_top_n_items = cum_cv_dfv_items[0:abs(self.top_n)]
            self.cv_raw = [cv_dfv[0] for cv_dfv in cv_dfv_top_n_items]
        else:
            self.cv_raw = list(self.cv_raw)
        # If we need to pareto, order the category values in pareto order.
        if self.pareto_term:
            pareto_cv_dfv_items = sorted(_pareto_by_cv.items(), 
                                         key = itemgetter(1) ,
                                         reverse = True)
            pareto_cv = [cv_dfv[0] for cv_dfv in pareto_cv_dfv_items]
            if self.top_n_term:
                self.cv_raw = [cv for cv in pareto_cv if cv in self.cv_raw]
            else:
                self.cv_raw = pareto_cv
            
            if self.mapf is None:
                self.cv = self.cv_raw
            else:
                self.cv = [self.mapf(cv) for cv in self.cv_raw]
        else:
            # otherwise, order them by sortf if there is one.
            if self.mapf is None:
                self.cv_raw.sort(key=self.sortf)
                self.cv = self.cv_raw
            else:
                self.cv = [self.mapf(cv) for cv in self.cv_raw]
                if self.mts: 
                    combined = sorted(zip(self.cv, self.cv_raw),key=self.sortf)
                    self.cv, self.cv_raw = zip(*combined)