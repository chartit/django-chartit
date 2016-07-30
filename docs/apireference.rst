==============
API Reference
==============

How to retrieve data
====================

DataPool
--------

.. automethod:: chartit.DataPool.__init__

PivotDataPool
-------------

.. automethod:: chartit.PivotDataPool.__init__

How to create the charts
========================

Chart
------

.. automethod:: chartit.Chart.__init__

PivotChart
----------

.. automethod:: chartit.PivotChart.__init__

How to use chartit django template filters
===========================================

.. autofunction:: chartit.templatetags.chartit.load_charts


Quick Reference for ``series`` and ``series_options``
=====================================================

+---------------------------------------------+-----------------------------------------------+
|         PivotDataPool series                |         PivotChart series_options             |
+=============================================+===============================================+
|::                                           |::                                             |
|                                             |                                               |
|  [{'options': {                             |  [{'options': {                               |
|      'source': SomeModel.objects.all(),     |      #any items from HighChart series. For ex.|
|      'top_n_per_cat': 10, ...               |      'type': 'column'                         |
|      }                                      |      },                                       |
|    'terms': {                               |    'terms': [                                 |
|      'any_name_here': Sum('a_valid_field'), |      'a_valid_term',                          |
|      'some_other_name':{                    |      'other_valid_term': {                    |
|        'func': Avg('a_valid_field),         |        #any options to override. For ex.      |
|        #any options to override             |        'type': 'area',                        |
|        ...                                  |        ...                                    |
|        },                                   |        },                                     |
|      ...                                    |      ...                                      |
|      }                                      |      ]                                        |
|   },                                        |    },                                         |
|   ... #repeat dicts with 'options' & 'terms'|    ... #repeat dicts with 'options' & 'terms' |
|   ]                                         |    ]                                          |
+---------------------------------------------+-----------------------------------------------+

+---------------------------------------------+-----------------------------------------------+
|         DataPool series                     |         Chart series_options                  |
+=============================================+===============================================+
|::                                           |::                                             |
|                                             |                                               |
|  [{'options': {                             |  [{'options': {                               |
|      'source': SomeModel.objects.all(),     |      #any items from HighChart series. For ex.|
|                                             |      'type': 'column'                         |
|      }                                      |      },                                       |
|    'terms': [                               |    'terms': {                                 |
|      'a_valid_field_name',                  |      'x_name': ['y_name', 'y_name', ...],     |
|      ..., # more valid field names          |      # only corresponding keys from DataPool  |
|      {'any_name': 'a_valid_field_name',     |      # terms are valid names.                 |
|       ... # more name:field_name pairs      |      ...                                      |
|       },                                    |                                               |
|      ]                                      |      }                                        |
|   },                                        |    },                                         |
|   ... #repeat dicts with 'options' & 'terms'|    ... #repeat dicts with 'options' & 'terms' |
|   ]                                         |    ]                                          |
+---------------------------------------------+-----------------------------------------------+
