import copy

from django.db.models.aggregates import Aggregate
from django.db.models.base import ModelBase
from django.db.models.manager import Manager
from django.db.models.query import QuerySet

from .exceptions import APIInputError


def _validate_field_lookup_term(model, term):
    """Checks whether the term is a valid field_lookup for the model.
    
    Args:
        model(django.db.models.Model): a django model for which to check 
            whether the term is a valid field_lookup.
        term(str): the term to check whether it is a valid field_lookup for the
            model supplied.
            
    Returns:
        True if term corresponds to a valid field_lookup for the model.
    
    Raises:
        FieldError: If the term supplied is not a valid field lookup parameter
            for the model.
    """
    # TODO: Memoization for speed enchancements
    terms = term.split('__')
    model_fields = model._meta.get_all_field_names()
    if terms[0] not in model_fields:
        raise APIInputError("Field %r does not exist. Valid lookups are %s." 
                         % (terms[0], ', '.join(model_fields)))
    if len(terms) == 1:
        return model._meta.get_field(terms[0]).verbose_name
    else:
        # DocString details for model._meta.get_field_by_name  
        # 
        # Returns a tuple (field_object, model, direct, m2m), where 
        #     field_object is the Field instance for the given name, 
        #     model is the model containing this field (None for 
        #         local fields), 
        #     direct is True if the field exists on this model, 
        #     and m2m is True for many-to-many relations. 
        # When 'direct' is False, 'field_object' is the corresponding 
        # RelatedObject for this field (since the field doesn't have 
        # an instance associated with it).
        field_details = model._meta.get_field_by_name(terms[0])
        # if the field is direct field
        if field_details[2]:
            m = field_details[0].related.parent_model
        else:
            m = field_details[0].model
        
        return _validate_field_lookup_term(m, '__'.join(terms[1:]))

def _clean_source(source):
    if isinstance(source, ModelBase):
        return source._base_manager.all()
    elif isinstance(source, Manager):
        return source.all()
    elif isinstance(source, QuerySet):
        return source
    raise APIInputError("'source' must either be a QuerySet, Model or "
                        "Manager. Got %s of type %s instead."  
                        %(source, type(source)))

def _validate_func(func):
    if not isinstance(func, Aggregate):
        raise APIInputError("'func' must an instance of django Aggregate. "
                            "Got %s of type %s instead" % (func, type(func)))

def _clean_categories(categories, source):
    if isinstance(categories, basestring):
        categories = [categories]
    elif isinstance(categories, (tuple, list)):
        if not categories:
            raise APIInputError("'categories' tuple or list must contain at " 
                                "least one valid model field. Got %s." 
                                %categories)
    else:
        raise APIInputError("'categories' must be one of the following "
                            "types: basestring, tuple or list. Got %s of "
                            "type %s instead."
                            %(categories, type(categories)))
    field_aliases = {}
    for c in categories:
        field_aliases[c] = _validate_field_lookup_term(source.model, c)
    return categories, field_aliases

def _clean_legend_by(legend_by, source):
    if isinstance(legend_by, basestring):
        legend_by = [legend_by]
    elif isinstance(legend_by, (tuple, list)):
        pass
    elif legend_by is None:
        legend_by = ()
    else:
        raise APIInputError("'legend_by' must be one of the following "
                            "types: basestring, tuple or list. Got %s of "
                            "type %s instead."
                            %(legend_by, type(legend_by)))
    field_aliases = {}
    for lg in legend_by:
        field_aliases[lg] = _validate_field_lookup_term(source.model, lg)
    return legend_by, field_aliases

def _validate_top_n_per_cat(top_n_per_cat):
    if not isinstance(top_n_per_cat,  int):
        raise APIInputError("'top_n_per_cat' must be an int. Got %s of type "
                            "%s instead." 
                            %(top_n_per_cat, type(top_n_per_cat)))

def _clean_field_aliases(fa_actual, fa_cat, fa_lgby):
    fa = copy.copy(fa_lgby)
    fa.update(fa_cat)
    fa.update(fa_actual)
    return fa

def _convert_pdps_to_dict(series_list):
    series_dict = {}
    for sd in series_list:
        try:
            options = sd['options']
        except KeyError:
            raise APIInputError("%s is missing the 'options' key." %sd)
        if not isinstance(options, dict):
            raise APIInputError("Expecting a dict in place of: %s" %options)
        
        try:
            terms = sd['terms']
        except KeyError:
            raise APIInputError("%s is missing have the 'terms' key." %sd)
        if isinstance(terms, dict):
            if not terms:
                raise APIInputError("'terms' cannot be empty.")
            for tk, tv in terms.items():
                if isinstance(tv, Aggregate):
                    tv = {'func': tv}
                elif isinstance(tv, dict):
                    pass
                else:
                    raise APIInputError("Expecting a dict or django Aggregate "
                                        "in place of: %s" %tv)
                opts = copy.deepcopy(options)
                opts.update(tv)
                series_dict.update({tk: opts})
        else:
            raise APIInputError("Expecting a dict in place of: %s" 
                                %terms)
    return series_dict

            
def clean_pdps(series):
    """Clean the PivotDataPool series input from the user.
    """
    if isinstance(series, list):
        series = _convert_pdps_to_dict(series)
        clean_pdps(series)
    elif isinstance(series, dict):
        if not series:
            raise APIInputError("'series' cannot be empty.")
        for td in series.values():
            # td is not a dict
            if not isinstance(td, dict):
                raise APIInputError("Expecting a dict in place of: %s" %td)
            # source
            try:
                td['source'] = _clean_source(td['source'])
            except KeyError:
                raise APIInputError("Missing 'source': %s" % td)
            # func
            try:
                _validate_func(td['func'])
            except KeyError:
                raise APIInputError("Missing 'func': %s" % td)
            # categories
            try:
                td['categories'], fa_cat = _clean_categories(td['categories'],
                                                            td['source'])
            except KeyError:
                raise APIInputError("Missing 'categories': %s" % td)
            # legend_by
            try:
                td['legend_by'], fa_lgby = _clean_legend_by(td['legend_by'],
                                                           td['source'])
            except KeyError:
                td['legend_by'], fa_lgby = (), {}
            # top_n_per_cat
            try:
                _validate_top_n_per_cat(td['top_n_per_cat'])
            except KeyError:
                td['top_n_per_cat'] = 0
            # field_aliases
            try:
                fa_actual = td['field_aliases']
            except KeyError:
                td['field_aliases'] = fa_actual = {}
            td['field_aliases'] = _clean_field_aliases(fa_actual, 
                                                       fa_cat, 
                                                       fa_lgby)
    else:
        raise APIInputError("Expecting a dict or list in place of: %s" %series)
    return series

def _convert_dps_to_dict(series_list):
    series_list = copy.deepcopy(series_list)
    series_dict = {}
    if not series_list:
        raise APIInputError("'series' cannot be empty.")
    for sd in series_list:
        try:
            options = sd['options']
        except KeyError:
            raise APIInputError("%s is missing the 'options' key." %sd)
        if not isinstance(options, dict):
            raise APIInputError("Expecting a dict in place of: %s" %options)
        
        try:
            terms = sd['terms']
        except KeyError:
            raise APIInputError("%s is missing the 'terms' key." %sd)
        if isinstance(terms, list):
            for term in terms:
                if isinstance(term, basestring):
                    series_dict[term] = copy.deepcopy(options)
                elif isinstance(term, dict):
                    for tk, tv in term.items():
                        if isinstance(tv, basestring):
                            opts = copy.deepcopy(options)
                            opts['field'] = tv
                            series_dict[tk] = opts
                        elif isinstance(tv, dict):
                            opts = copy.deepcopy(options)
                            opts.update(tv)
                            series_dict[tk] = opts 
                        else:
                            raise APIInputError("Expecting a basestring or "
                                                "dict in place of: %s" %tv)
        elif isinstance(terms, dict):
            for tk, tv in terms.items():
                if isinstance(tv, basestring):
                    opts = copy.deepcopy(options)
                    opts['field'] = tv
                    series_dict[tk] = opts
                elif isinstance(tv, dict):
                    opts = copy.deepcopy(options)
                    opts.update(tv)
                    series_dict[tk] = opts 
                else:
                    raise APIInputError("Expecting a basestring or dict in "
                                        "place of: %s" %tv)
        else:
            raise APIInputError("Expecting a list or dict in place of: %s." 
                                %terms)
    return series_dict

def clean_dps(series):
    """Clean the DataPool series input from the user.
    """
    if isinstance(series, dict):
        if not series:
            raise APIInputError("'series' cannot be empty.")
        for tk, td in series.items():
            try:
                td['source'] = _clean_source(td['source'])
            except KeyError:
                raise APIInputError("%s is missing the 'source' key." %td)
            td.setdefault('field', tk)
            fa = _validate_field_lookup_term(td['source'].model, td['field'])\
                   .title()
            # If the user supplied term is not a field name, use it as an alias
            if tk != td['field']:
                fa = tk 
            td.setdefault('field_alias', fa)
    elif isinstance(series, list):
        series = _convert_dps_to_dict(series)
        clean_dps(series)
    else:
        raise APIInputError("Expecting a dict or list in place of: %s" %series)
    return series

def _convert_pcso_to_dict(series_options):
    series_options_dict = {}
    for stod in series_options:
        try:
            options = stod['options']
        except KeyError:
            raise APIInputError("%s is missing the 'options' key." %stod)
        if not isinstance(options, dict):
            raise APIInputError("Expecting a dict in place of: %s" %options)
        
        try:
            terms = stod['terms']
        except KeyError:
            raise APIInputError("%s is missing the 'terms' key." %stod)
        if isinstance(terms, list):
            for term in terms:
                if isinstance(term, basestring):
                    opts = copy.deepcopy(options)
                    series_options_dict.update({term: opts})
                elif isinstance(term, dict):
                    for tk, tv in term.items():
                        if not isinstance(tv, dict):
                            raise APIInputError("Expecting a dict in place "
                                                "of: %s" %tv)
                        opts = copy.deepcopy(options)
                        opts.update(tv)
                        series_options_dict.update({tk: opts})
        else:
            raise APIInputError("Expecting a list in place of: %s" %terms)
    return series_options_dict


def clean_pcso(series_options, ds):
    """Clean the PivotChart series_options input from the user.
    """
    #todlist = term option dict list
    if isinstance(series_options, dict):
        for sok, sod in series_options.items():
            if sok not in ds.series.keys():
                    raise APIInputError("All the series terms must be present "
                                        "in the series dict of the "
                                        "datasource. Got %s. Allowed values "
                                        "are: %s" 
                                        %(sok, ', '.join(ds.series.keys())))
            if not isinstance(sod, dict):
                raise APIInputError("All the series options must be of the "
                                    "type dict. Got %s of type %s instead." 
                                    %(sod, type(sod)))
    elif isinstance(series_options, list):
        series_options = _convert_pcso_to_dict(series_options)
        clean_pcso(series_options, ds)
    else:
        raise APIInputError("Expecting a dict or list in place of: %s." 
                            %series_options)
    return series_options

def _convert_cso_to_dict(series_options):
    series_options_dict = {}
    #stod: series term and option dict
    for stod in series_options:
        try:
            options = stod['options']
        except KeyError:
            raise APIInputError("%s is missing the 'options' key." %stod)
        if not isinstance(options, dict):
            raise APIInputError("Expecting a dict in place of: %s" %options)
        
        try:
            terms = stod['terms']
        except KeyError:
            raise APIInputError("%s is missing the 'terms' key." %stod)
        
        if isinstance(terms, dict):
            if not terms:
                raise APIInputError("'terms' dict cannot be empty.")
            for tk, td in terms.items():
                if isinstance(td, list):
                    for yterm in td:
                        if isinstance(yterm, basestring):
                            opts = copy.deepcopy(options)
                            opts['_x_axis_term'] = tk
                            series_options_dict[yterm] = opts
                        elif isinstance(yterm, dict):
                            opts = copy.deepcopy(options)
                            opts.update(yterm.values()[0])
                            opts['_x_axis_term'] = tk
                            series_options_dict[yterm.keys()[0]] = opts
                        else:
                            raise APIInputError("Expecting a basestring or "
                                                "dict in place of: %s." %yterm)
                else:
                    raise APIInputError("Expecting a list instead of: %s"
                                        %td)
        else:
            raise APIInputError("Expecting a dict in place of: %s." 
                                %terms)
    return series_options_dict
                    
def clean_cso(series_options, ds):
    """Clean the Chart series_options input from the user.
    """
    if isinstance(series_options, dict):
        for sok, sod in series_options.items():
            if sok not in ds.series.keys():
                    raise APIInputError("%s is not one of the keys of the "
                                        "datasource series. Allowed values "
                                        "are: %s" 
                                        %(sok, ', '.join(ds.series.keys())))
            if not isinstance(sod, dict):
                raise APIInputError("%s is of type: %s. Expecting a dict." 
                                    %(sod, type(sod)))
            try:
                _x_axis_term = sod['_x_axis_term']
                if _x_axis_term not in ds.series.keys():
                    raise APIInputError("%s is not one of the keys of the "
                                        "datasource series. Allowed values "
                                        "are: %s" 
                                        %(_x_axis_term, 
                                          ', '.join(ds.series.keys())))
            except KeyError:
                raise APIInputError("Expecting a '_x_axis_term' for %s." %sod)
            if ds.series[sok]['_data'] != ds.series[_x_axis_term]['_data']:
                raise APIInputError("%s and %s do not belong to the same "
                                    "table." %(sok, _x_axis_term))
                sod['_data'] = ds.series[sok]['_data']
    elif isinstance(series_options, list):
        series_options = _convert_cso_to_dict(series_options)
        clean_cso(series_options, ds)
    else:
        raise APIInputError("'series_options' must either be a dict or a "
                            "list. Got %s of type %s instead." 
                            %(series_options, type(series_options)))
    return series_options

def clean_sortf_mapf_mts(sortf_mapf_mts):
    if sortf_mapf_mts is None:
        sortf_mapf_mts = (None, None, False)
    if isinstance(sortf_mapf_mts, tuple):
        if len(sortf_mapf_mts) != 3:
            raise APIInputError("%r must have exactly three elements."
                                %sortf_mapf_mts)
        sortf, mapf, mts = sortf_mapf_mts
        if not callable(sortf) and sortf is not None:
            raise APIInputError("%r must be callable or None." %sortf)
        if not callable(mapf) and mapf is not None:
            raise APIInputError("%r must be callable or None." %mapf)
        mts = bool(mts)
    return (sortf, mapf, mts)

def clean_x_sortf_mapf_mts(x_sortf_mapf_mts):
    cleaned_x_s_m_mts = []
    if x_sortf_mapf_mts is None:
        x_sortf_mapf_mts = [(None, None, False)]
    if isinstance(x_sortf_mapf_mts, tuple):
        x_sortf_mapf_mts = [x_sortf_mapf_mts]
    for x_s_m_mts in x_sortf_mapf_mts:
        if not isinstance(x_s_m_mts, tuple):
            raise APIInputError("%r must be a tuple." %x_s_m_mts)
        if len(x_s_m_mts) != 3:
            raise APIInputError("%r must have exactly three elements."
                                %x_s_m_mts)
        x_sortf = x_s_m_mts[0]
        if not callable(x_sortf) and x_sortf is not None:
            raise APIInputError("%r must be callable or None." %x_sortf)
        x_mapf = x_s_m_mts[1]
        if not callable(x_mapf) and x_mapf is not None:
            raise APIInputError("%r must be callable or None." %x_mapf)
        x_mts = bool(x_s_m_mts[2])
        cleaned_x_s_m_mts.append((x_sortf, x_mapf, x_mts))
    return cleaned_x_s_m_mts
