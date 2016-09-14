import sys
from django.test import TestCase, override_settings
from django.db.models import Avg, Sum

from chartit import PivotDataPool, DataPool, Chart, PivotChart
from chartit.exceptions import APIInputError
from chartit.templatetags import chartit
from chartit.validation import clean_pdps, clean_dps, clean_pcso, clean_cso

from demoproject.models import SalesHistory, MonthlyWeatherByCity, \
    MonthlyWeatherSeattle
from utils import assertOptionDictsEqual

TestCase.assertOptionDictsEqual = assertOptionDictsEqual


class GoodPivotSeriesDictInputTests(TestCase):

    def test_all_terms(self):
        series_input = \
          {'avg_price': {
             'source': SalesHistory.objects.all(),
             'func': Avg('price'),
             'categories': [
               'bookstore__city__state',
               'bookstore__city__city'],
             'legend_by': ['book__genre__name'],
             'top_n_per_cat': 5,
             'field_aliases': {
               'bookstore__city__state': 'state',
               'bookstore__city__city': 'city',
               'book__genre__name': 'name'}}}
        series_cleaned = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': [
                    'bookstore__city__state',
                    'bookstore__city__city'
                ],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 5,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'bookstore__city__city': 'city',
                    'book__genre__name': 'name'
                }
            }
        }
        self.assertOptionDictsEqual(clean_pdps(series_input),
                                    series_cleaned)

    def test_categories_is_a_str(self):
        series_input = \
          {'avg_price': {
             'source': SalesHistory.objects.all(),
             'func': Avg('price'),
             'categories': 'bookstore__city__state',
             'legend_by': ['book__genre__name'],
             'top_n_per_cat': 5,
             'field_aliases': {
               'bookstore__city__state': 'state',
               'book__genre__name': 'name'}}}
        series_cleaned = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': ['bookstore__city__state'],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 5,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'book__genre__name': 'name'
                }
            }
        }
        self.assertOptionDictsEqual(clean_pdps(series_input),
                                    series_cleaned)

    def test_legend_by_is_a_str(self):
        series_input = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': [
                    'bookstore__city__state',
                    'bookstore__city__city',
                ],
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 5,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'bookstore__city__city': 'city',
                    'book__genre__name': 'name'
                }
            }
        }
        series_cleaned = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': [
                    'bookstore__city__state',
                    'bookstore__city__city',
                ],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 5,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'bookstore__city__city': 'city',
                    'book__genre__name': 'name'
                }
            }
        }
        self.assertOptionDictsEqual(clean_pdps(series_input),
                                    series_cleaned)

    def test_no_legend_by(self):
        series_input = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': [
                    'bookstore__city__state',
                    'bookstore__city__city',
                ],
                'top_n_per_cat': 5,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'bookstore__city__city': 'city'
                }
            }
        }
        series_cleaned = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': [
                    'bookstore__city__state',
                    'bookstore__city__city',
                ],
                'legend_by': (),
                'top_n_per_cat': 5,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'bookstore__city__city': 'city'
                }
            }
        }
        self.assertOptionDictsEqual(clean_pdps(series_input),
                                    series_cleaned)

    def test_no_top_n_per_cat(self):
        series_input = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': [
                    'bookstore__city__state',
                    'bookstore__city__city'
                ],
                'legend_by': ['book__genre__name'],
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'bookstore__city__city': 'city',
                    'book__genre__name': 'name'
                }
            }
        }
        series_cleaned = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': [
                    'bookstore__city__state',
                    'bookstore__city__city'
                ],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 0,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'bookstore__city__city': 'city',
                    'book__genre__name': 'name'
                }
            }
        }
        self.assertOptionDictsEqual(clean_pdps(series_input),
                                    series_cleaned)

    def test_no_field_aliases(self):
        series_input = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': [
                    'bookstore__city__state',
                    'bookstore__city__city'
                ],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 5
            }
        }
        series_cleaned = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': [
                    'bookstore__city__state',
                    'bookstore__city__city'
                ],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 5,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'bookstore__city__city': 'city',
                    'book__genre__name': 'name'
                }
            }
        }
        self.assertOptionDictsEqual(clean_pdps(series_input),
                                    series_cleaned)

    def test_custom_field_aliases(self):
        series_input = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': [
                    'bookstore__city__state',
                    'bookstore__city__city'
                ],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 5,
                'field_aliases': {
                    'bookstore__city__state': 'St',
                    'bookstore__city__city': 'Cty',
                    'book__genre__name': 'Genre'
                }
            }
        }
        series_cleaned = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': [
                    'bookstore__city__state',
                    'bookstore__city__city'
                ],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 5,
                'field_aliases': {
                    'bookstore__city__state': 'St',
                    'bookstore__city__city': 'Cty',
                    'book__genre__name': 'Genre'
                }
            }
        }
        self.assertOptionDictsEqual(clean_pdps(series_input),
                                    series_cleaned)

    def test_partial_field_aliases(self):
        series_input = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': [
                    'bookstore__city__state',
                    'bookstore__city__city'
                ],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 5,
                'field_aliases': {
                    'bookstore__city__state': 'St'
                }
            }
        }
        series_cleaned = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': [
                    'bookstore__city__state',
                    'bookstore__city__city'
                ],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 5,
                'field_aliases': {
                    'bookstore__city__state': 'St',
                    'bookstore__city__city': 'city',
                    'book__genre__name': 'name'
                }
            }
        }
        self.assertOptionDictsEqual(clean_pdps(series_input),
                                    series_cleaned)


class BadPivotSeriesDictInputTests(TestCase):

    def test_series_not_dict_or_list(self):
        series_input = 'foobar'
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_func_dict_wrong_type(self):
        series_input = {'avg_price': 'foobar'}
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_source_missing(self):
        series_input = \
          {'avg_price': {
             'func': Avg('price'),
             'categories': ['bookstore__city__state', 'bookstore__city__city'],
             'legend_by': ['book__genre__name'],
             'top_n_per_cat': 5,
             'field_aliases': {
               'bookstore__city__state': 'state',
               'bookstore__city__city': 'city',
               'book__genre__name': 'name'}}}
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_source_wrong_type(self):
        series_input = \
          {'avg_price': {
             'source': 'foobar',
             'func': Avg('price'),
             'categories': ['bookstore__city__state', 'bookstore__city__city'],
             'legend_by': ['book__genre__name'],
             'top_n_per_cat': 5,
             'field_aliases': {
               'bookstore__city__state': 'state',
               'bookstore__city__city': 'city',
               'book__genre__name': 'name'}}}
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_func_missing(self):
        series_input = \
          {'avg_price': {
             'source': SalesHistory.objects.all(),
             'categories': ['bookstore__city__state', 'bookstore__city__city'],
             'legend_by': ['book__genre__name'],
             'top_n_per_cat': 5,
             'field_aliases': {
               'bookstore__city__state': 'state',
               'bookstore__city__city': 'city',
               'book__genre__name': 'name'}}}
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_func_wrong_type(self):
        series_input = \
          {'avg_price': {
             'source': SalesHistory.objects.all(),
             'func': 'foobar',
             'categories': ['bookstore__city__state', 'bookstore__city__city'],
             'legend_by': ['book__genre__name'],
             'top_n_per_cat': 5,
             'field_aliases': {
               'bookstore__city__state': 'state',
               'bookstore__city__city': 'city',
               'book__genre__name': 'name'}}}
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_categories_missing(self):
        series_input = \
          {'avg_price': {
             'source': SalesHistory.objects.all(),
             'func': Avg('price'),
             'legend_by': ['book__genre__name'],
             'top_n_per_cat': 5,
             'field_aliases': {
               'bookstore__city__state': 'state',
               'bookstore__city__city': 'city',
               'book__genre__name': 'name'}}}
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_categories_wrong_type(self):
        series_input = \
          {'avg_price': {
             'source': SalesHistory.objects.all(),
             'func': Avg('price'),
             'categories': 0,
             'legend_by': ['book__genre__name'],
             'top_n_per_cat': 5,
             'field_aliases': {
               'bookstore__city__state': 'state',
               'bookstore__city__city': 'city',
               'book__genre__name': 'name'}}}
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_categories_not_a_valid_field(self):
        series_input = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': ['foobar'],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 5,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'bookstore__city__city': 'city',
                    'book__genre__name': 'name'
                }
            }
        }
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_categories_empty_list(self):
        series_input = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': [],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 5,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'bookstore__city__city': 'city',
                    'book__genre__name': 'name'
                }
            }
        }
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_legend_by_wrong_type(self):
        series_input = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': 'foobar',
                'categories': [
                    'bookstore__city__state',
                    'bookstore__city__city',
                ],
                'legend_by': 10,
                'top_n_per_cat': 5,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'bookstore__city__city': 'city',
                    'book__genre__name': 'name'
                }
            }
        }
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_legend_by_not_a_valid_field(self):
        series_input = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': 'foobar',
                'categories': [
                    'bookstore__city__state',
                    'bookstore__city__city',
                ],
                'legend_by': ['foobar'],
                'top_n_per_cat': 5,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'bookstore__city__city': 'city',
                    'book__genre__name': 'name'
                }
            }
        }
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_top_n_per_cat_wrong_type(self):
        series_input = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': 'foobar',
                'categories': [
                    'bookstore__city__state',
                    'bookstore__city__city',
                ],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 'foobar',
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'bookstore__city__city': 'city',
                    'book__genre__name': 'name'
                }
            }
        }
        self.assertRaises(APIInputError, clean_pdps, series_input)


class GoodPivotSeriesListInputTests(TestCase):

    def test_all_terms(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all(),
                'categories': 'bookstore__city__state',
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 2
            },
            'terms': {
                'avg_price': Avg('price'),
                'avg_price_all': {
                    'func': Avg('price'),
                    'legend_by': None
                }
            }
        }]
        series_cleaned = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': ['bookstore__city__state'],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 2,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'book__genre__name': 'name'
                }
            },
            'avg_price_all': {
                'func': Avg('price'),
                'source': SalesHistory.objects.all(),
                'categories': ['bookstore__city__state'],
                'legend_by': (),
                'top_n_per_cat': 2,
                'field_aliases': {
                    'bookstore__city__state': 'state'
                }
            }
        }
        self.assertOptionDictsEqual(clean_pdps(series_input),
                                    series_cleaned)

    def test_source_a_manager(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects,
                'categories': 'bookstore__city__state',
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 2
            },
            'terms': {
                'avg_price': Avg('price'),
                'avg_price_all': {
                    'func': Avg('price'),
                    'legend_by': None
                }
            }
        }]
        series_cleaned = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': ['bookstore__city__state'],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 2,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'book__genre__name': 'name'
                }
            },
            'avg_price_all': {
                'func': Avg('price'),
                'source': SalesHistory.objects.all(),
                'categories': ['bookstore__city__state'],
                'legend_by': (),
                'top_n_per_cat': 2,
                'field_aliases': {
                    'bookstore__city__state': 'state'
                }
            }
        }
        self.assertOptionDictsEqual(clean_pdps(series_input),
                                    series_cleaned)

    def test_source_a_model(self):
        series_input = [{
            'options': {
                'source': SalesHistory,
                'categories': 'bookstore__city__state',
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 2
            },
            'terms': {
                'avg_price': Avg('price'),
                'avg_price_all': {
                    'func': Avg('price'),
                    'legend_by': None
                }
            }
        }]
        series_cleaned = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': ['bookstore__city__state'],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 2,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'book__genre__name': 'name'
                }
            },
            'avg_price_all': {
                'func': Avg('price'),
                'source': SalesHistory.objects.all(),
                'categories': ['bookstore__city__state'],
                'legend_by': (),
                'top_n_per_cat': 2,
                'field_aliases': {
                    'bookstore__city__state': 'state'
                }
            }
        }
        self.assertOptionDictsEqual(clean_pdps(series_input),
                                    series_cleaned)

    def test_term_opts_an_aggr(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all(),
                'categories': ['bookstore__city__state'],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 2
            },
            'terms': {
                'avg_price': Avg('price')
            }
        }]
        series_cleaned = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': ['bookstore__city__state'],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 2,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'book__genre__name': 'name'
                }
            }
        }
        self.assertOptionDictsEqual(clean_pdps(series_input),
                                    series_cleaned)

    def test_term_opts_a_dict(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all(),
                'categories': 'bookstore__city__state',
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 2
            },
            'terms': {
                'avg_price': {
                    'func': Avg('price'),
                    'top_n_per_cat': 3
                }
            }
        }]
        series_cleaned = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': ['bookstore__city__state'],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 3,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'book__genre__name': 'name'
                }
            }
        }
        self.assertOptionDictsEqual(clean_pdps(series_input),
                                    series_cleaned)

    def test_opts_empty(self):
        series_input = [{
            'options': {},
            'terms': {
                'avg_price': {
                    'source': SalesHistory.objects.all(),
                    'categories': ['bookstore__city__state'],
                    'func': Avg('price'),
                    'top_n_per_cat':3
                }
            }
        }]
        series_cleaned = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': ['bookstore__city__state'],
                'legend_by': (),
                'top_n_per_cat': 3,
                'field_aliases': {
                    'bookstore__city__state': 'state'
                }
            }
        }
        self.assertOptionDictsEqual(clean_pdps(series_input),
                                    series_cleaned)

    def test_categories_a_str(self):
        series_input = [{
            'options': {},
            'terms': {
                'avg_price': {
                    'source': SalesHistory.objects.all(),
                    'categories': 'bookstore__city__state',
                    'func': Avg('price'),
                    'top_n_per_cat': 3
                }
            }
        }]
        series_cleaned = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': ['bookstore__city__state'],
                'legend_by': (),
                'top_n_per_cat': 3,
                'field_aliases': {
                    'bookstore__city__state': 'state'
                }
            }
        }
        self.assertOptionDictsEqual(clean_pdps(series_input),
                                    series_cleaned)

    def test_legend_by_a_str(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all(),
                'categories': ['bookstore__city__state'],
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 2
            },
            'terms': {
                'avg_price': Avg('price')
            }
        }]
        series_cleaned = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': ['bookstore__city__state'],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 2,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'book__genre__name': 'name'
                }
            }
        }
        self.assertOptionDictsEqual(clean_pdps(series_input),
                                    series_cleaned)

    def test_multiple_dicts(self):
        series_input = [
            {
                'options': {
                    'source': SalesHistory.objects.all(),
                    'categories': 'bookstore__city__state',
                    'legend_by': 'book__genre__name',
                    'top_n_per_cat': 2
                },
                'terms': {
                    'avg_price': Avg('price')
                }
            }, {
                'options': {
                    'source': SalesHistory.objects.filter(price__gte=10),
                    'categories': 'bookstore__city__city',
                    'top_n_per_cat': 2
                },
                'terms': {
                    'avg_price_high': {
                        'func': Avg('price'),
                        'legend_by': None
                    }
                }
            }
        ]
        series_cleaned = {
            'avg_price': {
                'source': SalesHistory.objects.all(),
                'func': Avg('price'),
                'categories': ['bookstore__city__state'],
                'legend_by': ['book__genre__name'],
                'top_n_per_cat': 2,
                'field_aliases': {
                    'bookstore__city__state': 'state',
                    'book__genre__name': 'name'
                }
            },
            'avg_price_high': {
                'func': Avg('price'),
                'source': SalesHistory.objects.filter(price__gte=10),
                'categories': ['bookstore__city__city'],
                'legend_by': (),
                'top_n_per_cat': 2,
                'field_aliases': {
                    'bookstore__city__city': 'city'
                }
            }
        }
        self.assertOptionDictsEqual(clean_pdps(series_input),
                                    series_cleaned)


class BadPivotSeriesListInputTests(TestCase):

    def test_terms_empty(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all(),
                'categories': 'bookstore__city__state',
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 2
            },
            'terms': {}
        }]
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_terms_missing(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all(),
                'categories': 'bookstore__city__state',
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 2
            }
        }]
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_terms_a_list_not_a_dict(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all(),
                'categories': 'bookstore__city__state',
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 2
            },
            'terms': [{
                'avg_price': Avg('price'),
                'avg_price_all': {
                    'func': Avg('price'),
                    'legend_by': None
                }
            }]
        }]
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_source_missing(self):
        series_input = [{
            'options': {
                'categories': 'bookstore__city__state',
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 2
            },
            'terms': {
                'avg_price': Avg('price'),
                'avg_price_all': {
                    'func': Avg('price'),
                    'legend_by': None
                }
            }
        }]
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_options_missing(self):
        series_input = [{
            'terms': {
                'avg_price': Avg('price'),
                'avg_price_all': {
                    'func': Avg('price'),
                    'legend_by': None
                }
            }
        }]
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_options_empty(self):
        series_input = [{
            'options': {},
            'terms': {
                'avg_price': Avg('price'),
                'avg_price_all': {
                    'func': Avg('price'),
                    'legend_by': None
                }
            }
        }]
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_source_wrong_type(self):
        series_input = [{
            'options': {
                'source': 'foobar',
                'categories': 'bookstore__city__state',
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 2
            },
            'terms': {
                'avg_price': Avg('price'),
                'avg_price_all': {
                    'func': Avg('price'),
                    'legend_by': None
                }
            }
        }]
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_categories_wrong_type(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all(),
                'categories': 10,
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 2
            },
            'terms': {
                'avg_price': Avg('price'),
                'avg_price_all': {
                    'func': Avg('price'),
                    'legend_by': None
                }
            }
        }]
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_categories_not_a_field(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all(),
                'categories': 'foobar',
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 2
            },
            'terms': {
                'avg_price': Avg('price'),
                'avg_price_all': {
                    'func': Avg('price'),
                    'legend_by': None
                }
            }
        }]
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_legend_by_wrong_type(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all(),
                'categories': 'bookstore__city__state',
                'legend_by': 10,
                'top_n_per_cat': 2
            },
            'terms': {
                'avg_price': Avg('price'),
                'avg_price_all': {
                    'func': Avg('price'),
                    'legend_by': None
                }
            }
        }]
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_legend_by_not_a_field(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all(),
                'categories': 'bookstore__city__state',
                'legend_by': 'foobar',
                'top_n_per_cat': 2
            },
            'terms': {
                'avg_price': Avg('price'),
                'avg_price_all': {
                    'func': Avg('price'),
                    'legend_by': None
                }
            }
        }]
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_term_func_wrong_type(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all(),
                'categories': 'bookstore__city__state',
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 2
            },
            'terms': {
                'avg_price': 'foobar',
                'avg_price_all': {
                    'func': Avg('price'),
                    'legend_by': None
                }
            }
        }]
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_term_dict_func_wrong_type(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all(),
                'categories': 'bookstore__city__state',
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 2
            },
            'terms': {
                'avg_price': Avg('price'),
                'avg_price_all': {
                    'func': 'foobar',
                    'legend_by': None
                }
            }
        }]
        self.assertRaises(APIInputError, clean_pdps, series_input)

    def test_term_dict_legend_by_wrong_type(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all(),
                'categories': 'bookstore__city__state',
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 2
            },
            'terms': {
                'avg_price': Avg('price'),
                'avg_price_all': {
                    'func': Avg('price'),
                    'legend_by': 10
                }
            }
        }]
        self.assertRaises(APIInputError, clean_pdps, series_input)


class GoodDataSeriesListInputTests(TestCase):

    def test_all_terms(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all()
            },
            'terms': [
                'price',
                {
                    'genre': {
                        'field': 'book__genre__name',
                        'source': SalesHistory.objects.filter(price__gte=10),
                        'field_alias': 'gnr'
                    }
                }
            ]
        }]
        series_cleaned = {
            'price': {
                'source': SalesHistory.objects.all(),
                'field': 'price',
                'field_alias': 'price'
            },
            'genre': {
                'source': SalesHistory.objects.filter(price__gte=10),
                'field': 'book__genre__name',
                'field_alias': 'gnr'
            }
        }
        self.assertOptionDictsEqual(clean_dps(series_input),
                                    series_cleaned)

    def test_terms_list_all_str(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all()
            },
            'terms': ['price', 'book__genre__name']
        }]
        series_cleaned = {
            'price': {
                'source': SalesHistory.objects.all(),
                'field': 'price',
                'field_alias': 'price'
            },
            'book__genre__name': {
                'source': SalesHistory.objects.all(),
                'field': 'book__genre__name',
                'field_alias': 'name'
            }
        }
        self.assertOptionDictsEqual(clean_dps(series_input),
                                    series_cleaned)

    def test_terms_is_a_dict(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all()
            },
            'terms': {'price': {}}
        }]
        series_cleaned = {
            'price': {
                'source': SalesHistory.objects.all(),
                'field': 'price',
                'field_alias': 'price'
            }
        }
        self.assertOptionDictsEqual(clean_dps(series_input),
                                    series_cleaned)

    def test_terms_is_a_list_of_tuples_w_lambda(self):
        _l = lambda x: -x # noqa
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all()
            },
            'terms': [('price', _l)]
        }]
        series_cleaned = {
            'price': {
                'source': SalesHistory.objects.all(),
                'field': 'price',
                'field_alias': 'price',
                'fn': _l
            }
        }
        self.assertOptionDictsEqual(clean_dps(series_input),
                                    series_cleaned)

    def test_terms_is_a_list_of_tuples_containing_dict_and_lambda(self):
        _l = lambda x: -x # noqa
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all()
            },
            'terms': [({'price-x': 'price'}, _l)]
        }]
        series_cleaned = {
            'price-x': {
                'source': SalesHistory.objects.all(),
                'field': 'price',
                'field_alias': 'price-x',
                'fn': _l
            }
        }
        self.assertOptionDictsEqual(clean_dps(series_input),
                                    series_cleaned)

    def test_multiple_dicts(self):
        series_input = [
            {
                'options': {
                    'source': SalesHistory.objects.all()
                },
                'terms': ['price']
            }, {
                'options': {
                    'source': SalesHistory.objects.filter(price__gte=10)
                },
                'terms': {
                    'genre': {
                        'field': 'book__genre__name',
                        'field_alias': 'gnr'
                    }
                }
            }
        ]
        series_cleaned = {
            'price': {
                'source': SalesHistory.objects.all(),
                'field': 'price',
                'field_alias': 'price'
            },
            'genre': {
                'source': SalesHistory.objects.filter(price__gte=10),
                'field': 'book__genre__name',
                'field_alias': 'gnr'
            }
        }
        self.assertOptionDictsEqual(clean_dps(series_input),
                                    series_cleaned)


class BadDataSeriesListInputTests(TestCase):
    def test_source_missing(self):
        series_input = [{
            'options': {},
            'terms': [
                'price', {
                    'genre': {
                        'field': 'book__genre__name',
                        'source': SalesHistory.objects.filter(price__gte=10),
                        'field_alias': 'gnr'
                    }
                }
            ]
        }]
        self.assertRaises(APIInputError, clean_dps, series_input)

    def test_source_wrong_type(self):
        series_input = [{
            'options': {
                'source': 'foobar'
            },
            'terms': [
                'price', {
                    'genre': {
                        'field': 'book__genre__name',
                        'source': SalesHistory.objects.filter(price__gte=10),
                        'field_alias': 'gnr'
                    }
                }
            ]
        }]
        self.assertRaises(APIInputError, clean_dps, series_input)

    def test_series_terms_empty(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all()
            },
            'terms': []
        }]
        self.assertRaises(APIInputError, clean_dps, series_input)

    def test_series_terms_wrong_type(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all()
            },
            'terms': 'foobar'
        }]
        self.assertRaises(APIInputError, clean_dps, series_input)

    def test_terms_element_wrong_type(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all()
            },
            'terms': [10]
        }]
        self.assertRaises(APIInputError, clean_dps, series_input)

    def test_terms_element_not_a_field(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all()
            },
            'terms': [
                'foobar', {
                    'genre': {
                        'field': 'book__genre__name',
                        'source': SalesHistory.objects.filter(price__gte=10),
                        'field_alias': 'gnr'
                    }
                }
            ]
        }]
        self.assertRaises(APIInputError, clean_dps, series_input)


class GoodPivotChartOptionsTests(TestCase):

    def setUp(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all(),
                'categories': 'bookstore__city__state',
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 2
            },
            'terms': {
                'avg_price': Avg('price'),
                'avg_price_all': {
                    'func': Avg('price'),
                    'legend_by': None
                }
            }
        }]
        self.ds = PivotDataPool(series_input)

    def test_all_terms(self):
        pcso_input = [{
            'options': {
                'type': 'column'
            },
            'terms': [
                'avg_price',
                {
                    'avg_price_all': {
                        'type': 'area'
                    }
                }
            ]
        }]
        series_cleaned = {
            'avg_price': {
                'type': 'column'
            },
            'avg_price_all': {
                'type': 'area'
            }
        }
        self.assertOptionDictsEqual(clean_pcso(pcso_input, self.ds),
                                    series_cleaned)


class BadPivotChartOptionsTests(TestCase):

    def setUp(self):
        series_input = [{
            'options': {
                'source': SalesHistory.objects.all(),
                'categories': 'bookstore__city__state',
                'legend_by': 'book__genre__name',
                'top_n_per_cat': 2
            },
            'terms': {
                'avg_price': Avg('price'),
                'avg_price_all': {
                    'func': Avg('price'),
                    'legend_by': None
                }
            }
        }]
        self.ds = PivotDataPool(series_input)

    def test_term_not_in_pdps(self):
        pcso_input = [{
            'options': {
                'type': 'column'
            },
            'terms': [
                'foobar',
                {
                    'avg_price_all': {
                        'type': 'area'
                    }
                }
            ]
        }]
        self.assertRaises(APIInputError, clean_pcso, pcso_input, self.ds)

    def test_opts_missing(self):
        pcso_input = \
          [{'terms': [
              'avg_price',
              {'avg_price_all': {
                 'type': 'area'}}]}
           ]
        self.assertRaises(APIInputError, clean_pcso, pcso_input, self.ds)

    def test_opts_wrong_type(self):
        pcso_input = \
          [{'options': 0,
            'terms': [
              'avg_price',
              {'avg_price_all': {
                 'type': 'area'}}]}
           ]
        self.assertRaises(APIInputError, clean_pcso, pcso_input, self.ds)

    def test_terms_missing(self):
        pcso_input = \
          [{'opts': {
              'type': 'column'}}]
        self.assertRaises(APIInputError, clean_pcso, pcso_input, self.ds)

    def test_terms_a_dict_not_a_list(self):
        pcso_input = \
          [{'options': {
              'type': 'column'},
            'terms':
              {'avg_price_all': {
                 'type': 'area'}}}]
        self.assertRaises(APIInputError, clean_pcso, pcso_input, self.ds)

    def test_terms_a_str(self):
        pcso_input = \
          [{'options': {
              'type': 'column'},
            'terms':
              'foobar'}]
        self.assertRaises(APIInputError, clean_pcso, pcso_input, self.ds)


class GoodChartOptionsTests(TestCase):

    def setUp(self):
        series_input = \
          [{'options': {
              'source': MonthlyWeatherByCity.objects.all()},
            'terms': [
              'month',
              'boston_temp',
              'houston_temp',
              'new_york_temp']},
           {'options': {
              'source': MonthlyWeatherSeattle.objects.all()},
            'terms': [
              {'month_seattle': 'month'},
              'seattle_temp']
            }]
        self.ds = DataPool(series_input)

    def test_all_terms(self):
        so_input = [{
            'options': {
                'type': 'column'
            },
            'terms': {
                'month': [
                    'boston_temp', {
                        'new_york_temp': {
                            'type': 'area',
                            'xAxis': 1
                        }
                    }
                ],
                'month_seattle': ['seattle_temp']
            }
        }]
        so_cleaned = {
            'boston_temp': {
                '_x_axis_term': 'month',
                'type': 'column'
            },
            'new_york_temp': {
                '_x_axis_term': 'month',
                'type': 'area',
                'xAxis': 1
            },
            'seattle_temp': {
                '_x_axis_term': 'month_seattle',
                'type': 'column'
            }
        }
        self.assertOptionDictsEqual(clean_cso(so_input, self.ds),
                                    so_cleaned)

    def test_all_terms_str(self):
        so_input = [{
            'options': {
                'type': 'column'
            },
            'terms': {
                'month': ['boston_temp', 'new_york_temp']
            }
        }]
        so_cleaned = {
            'boston_temp': {
                '_x_axis_term': 'month',
                'type': 'column'
            },
            'new_york_temp': {
                '_x_axis_term': 'month',
                'type': 'column'
            }
        }
        self.assertOptionDictsEqual(clean_cso(so_input, self.ds),
                                    so_cleaned)

    def test_all_terms_dict(self):
        so_input = [
            {
                'options': {'type': 'column'},
                'terms': {
                    'month': [{
                        'boston_temp': {
                            'type': 'area',
                            'xAxis': 1
                        }}, {
                        'new_york_temp': {
                            'xAxis': 0
                        }}
                    ]
                }
            }
        ]
        so_cleaned = {
            'boston_temp': {
                '_x_axis_term': 'month',
                'type': 'area',
                'xAxis': 1
            },
            'new_york_temp': {
                '_x_axis_term': 'month',
                'type': 'column',
                'xAxis': 0
            }
        }
        self.assertOptionDictsEqual(clean_cso(so_input, self.ds),
                                    so_cleaned)

    def test_multiple_items_in_list(self):
        so_input = [
            {
                'options': {
                    'type': 'column'
                },
                'terms': {
                    'month': ['boston_temp', 'new_york_temp']
                }
            }, {
                'options': {
                    'type': 'area'
                },
                'terms': {
                    'month_seattle': ['seattle_temp']
                }
            }
        ]
        so_cleaned = {
            'boston_temp': {
                '_x_axis_term': 'month',
                'type': 'column'
            },
            'new_york_temp': {
                '_x_axis_term': 'month',
                'type': 'column'
            },
            'seattle_temp': {
                '_x_axis_term': 'month_seattle',
                'type': 'area'
            }
        }
        self.assertOptionDictsEqual(clean_cso(so_input, self.ds),
                                    so_cleaned)


class BadChartOptionsTests(TestCase):

    def setUp(self):
        series_input = \
          [{'options': {
              'source': MonthlyWeatherByCity.objects.all()},
            'terms': [
              'month',
              'boston_temp',
              'houston_temp',
              'new_york_temp']},
           {'options': {
              'source': MonthlyWeatherSeattle.objects.all()},
            'terms': [
              {'month_seattle': 'month'},
              'seattle_temp']
            }]
        self.ds = DataPool(series_input)

    def test_options_missing(self):
        so_input = [{
            'terms': {
                'month': [
                    'boston_temp', {
                        'new_york_temp': {
                            'type': 'area',
                            'xAxis': 1
                        }
                    }
                ],
                'month_seattle': ['seattle_temp']
            }
        }]
        self.assertRaises(APIInputError, clean_cso, so_input, self.ds)

    def test_options_wrong_type(self):
        so_input = [{
            'options': 10,
            'terms': {
                'month': [
                    'boston_temp', {
                        'new_york_temp': {
                            'type': 'area',
                            'xAxis': 1
                        }
                    }
                ],
                'month_seattle': ['seattle_temp']
            }
        }]
        self.assertRaises(APIInputError, clean_cso, so_input, self.ds)

    def test_terms_missing(self):
        so_input = \
          [{'options': {
              'type': 'line'}
            }]
        self.assertRaises(APIInputError, clean_cso, so_input, self.ds)

    def test_terms_wrong_type(self):
        so_input = \
          [{'options': {
              'type': 'line'},
            'terms': 10
            }]
        self.assertRaises(APIInputError, clean_cso, so_input, self.ds)

    def test_terms_a_list_not_a_dict(self):
        so_input = \
          [{'options': {
              'type': 'line'},
            'terms': [{
              'month': ['new_york_temp']}]
            }]
        self.assertRaises(APIInputError, clean_cso, so_input, self.ds)

    def test_terms_empty(self):
        so_input = \
          [{'options': {
              'type': 'line'},
            'terms': {}
            }]
        self.assertRaises(APIInputError, clean_cso, so_input, self.ds)

    def test_yterms_not_in_ds(self):
        so_input = \
          [{'options': {
              'type': 'column'},
            'terms': {
              'month': [
                 'foobar']}
            }]
        self.assertRaises(APIInputError, clean_cso, so_input, self.ds)

    def test_xterms_not_in_ds(self):
        so_input = \
          [{'options': {
              'type': 'column'},
            'terms': {
              'foobar': [
                 'seattle_temp']}
            }]
        self.assertRaises(APIInputError, clean_cso, so_input, self.ds)

    def test_yterms_not_a_list(self):
        so_input = \
          [{'options': {
              'type': 'column'},
            'terms': {
              'month': 'new_york_temp'}
            }]
        self.assertRaises(APIInputError, clean_cso, so_input, self.ds)


class ChartitTemplateTagTests(TestCase):

    def test_load_charts_with_None_chart(self):
        html = chartit.load_charts(None, 'my_chart')

        self.assertIn('<script type="text/javascript">', html)
        self.assertIn('var _chartit_hco_array = ();', html)
        self.assertIn('<script src="/static/chartit/js/chartloader.js" type="text/javascript">', html) # noqa

    def test_load_charts_with_missing_render_to(self):
        chart_data = DataPool(series=[{'options': {
            'source': SalesHistory.objects.all()},
            'terms': ['price', 'sale_date']
        }])

        chart = Chart(
            datasource=chart_data,
            series_options=[{
                'options': {
                    'type': 'column',
                    'stacking': False
                },
                'terms': {'sale_date': ['price']}}])

        html = chartit.load_charts(chart, '')

        self.assertIn('<script type="text/javascript">', html)
        self.assertIn('{"renderTo": "container"}', html)
        self.assertIn('"title": {"text": "Price vs. Sale Date"}', html)
        self.assertIn('<script src="/static/chartit/js/chartloader.js" type="text/javascript">', html) # noqa

    def test_load_charts_with_single_chart(self):
        chart_data = DataPool(series=[{'options': {
            'source': SalesHistory.objects.all()},
            'terms': ['price', 'sale_date']
        }])

        chart = Chart(
            datasource=chart_data,
            series_options=[{
                'options': {
                    'type': 'column',
                    'stacking': False
                },
                'terms': {'sale_date': ['price']}}])

        html = chartit.load_charts(chart, 'my_chart')

        self.assertIn('<script type="text/javascript">', html)
        self.assertIn('"stacking": false', html)
        self.assertIn('"type": "column"', html)
        self.assertIn('"name": "price"', html)
        self.assertIn('{"renderTo": "my_chart"}', html)
        self.assertIn('"title": {"text": "Price vs. Sale Date"}', html)
        self.assertIn('<script src="/static/chartit/js/chartloader.js" type="text/javascript">', html) # noqa

    def test_load_charts_with_two_charts(self):
        chart_data = DataPool(series=[{'options': {
            'source': SalesHistory.objects.all()},
            'terms': ['price', 'sale_date']
        }])

        chart = Chart(
            datasource=chart_data,
            series_options=[{
                'options': {
                    'type': 'column',
                    'stacking': False
                },
                'terms': {'sale_date': ['price']}}])

        pivot_input = [{
            'options': {
                'source': SalesHistory.objects.all(),
                'categories': 'bookstore__city__city',
            },
            'terms': {
                'avg_price': Avg('price'),
            }
        }]
        pivot_chart_data = PivotDataPool(pivot_input)

        pivot_chart = PivotChart(
            datasource=pivot_chart_data,
            series_options=[{
                'options': {
                    'type': 'column',
                    'stacking': False
                },
                'terms': ['avg_price']
            }]
        )

        html = chartit.load_charts([chart, pivot_chart],
                                   'my_chart,my_pivot_chart')

        self.assertIn('<script type="text/javascript">', html)
        self.assertIn('"stacking": false', html)
        self.assertIn('"type": "column"', html)
        self.assertIn('"name": "price"', html)
        # the first chart
        self.assertIn('{"renderTo": "my_chart"}', html)
        self.assertIn('"title": {"text": "Price vs. Sale Date"}', html)
        # the second chart
        self.assertIn('{"renderTo": "my_pivot_chart"}', html)
        self.assertIn('"title": {"text": "Avg_Price vs. City"}', html)
        self.assertIn('<script src="/static/chartit/js/chartloader.js" type="text/javascript">', html) # noqa

    def test_sortf_mapf_mts_with_data(self):
        """
            Test that PivotChart loads when there is actual data and
            sortf_mapf_mtp is specified!
        """

        def region_state(x):
            region = {'CA': 'S', 'MA': 'N', 'TX': 'S', 'NY': 'N'}
            return (region[x[0]], x[1])

        ds = PivotDataPool(
            series=[{
                'options': {
                    'source': SalesHistory.objects.all(),
                    'categories': [
                        'bookstore__city__state',
                        'bookstore__city__city'
                    ],
                    'legend_by': 'book__genre__name'
                },
                'terms': {
                    'tot_sales': Sum('sale_qty')
                }
            }],
            sortf_mapf_mts=(None, region_state, True)
        )

        chart = PivotChart(
            datasource=ds,
            series_options=[{
                'options': {
                    'type': 'column',
                    'stacking': True
                },
                'terms': ['tot_sales']
            }]
        )

        # just make sure this renders fine w/o errors
        html = chartit.load_charts([chart], 'my_chart')
        self.assertNotEqual(html, '')

    def test_sortf_mapf_mts_without_data(self):
        """
            Test that PivotChart loads when the QuerySet returns empty data and
            sortf_mapf_mtp is specified!
        """

        def region_state(x):
            region = {'CA': 'S', 'MA': 'N', 'TX': 'S', 'NY': 'N'}
            return (region[x[0]], x[1])

        ds = PivotDataPool(
            series=[{
                'options': {
                    'source': SalesHistory.objects.filter(
                                bookstore__city__city='TEST CITY'),
                    'categories': [
                        'bookstore__city__state',
                        'bookstore__city__city'
                    ],
                    'legend_by': 'book__genre__name'
                },
                'terms': {
                    'tot_sales': Sum('sale_qty')
                }
            }],
            sortf_mapf_mts=(None, region_state, True)
        )

        chart = PivotChart(
            datasource=ds,
            series_options=[{
                'options': {
                    'type': 'column',
                    'stacking': True
                },
                'terms': ['tot_sales']
            }]
        )

        # just make sure this renders fine w/o errors
        html = chartit.load_charts([chart], 'my_chart')
        self.assertNotEqual(html, '')


class ChartitJSRelPathTests(TestCase):
    """
        Test the CHARTIT_JS_REL_PATH setting.
    """

    def setUp(self):
        super(ChartitJSRelPathTests, self).setUp()

        # force chartit module to reload
        # b/c this setting is evaluated near the top
        for mod in ['chartit.templatetags.chartit',
                    'chartit.templatetags',
                    'chartit']:
            if mod in sys.modules:
                del sys.modules[mod]

    @override_settings(CHARTIT_JS_REL_PATH='chartit/js/')
    def test_setting_starting_without_slash(self):
        from chartit.templatetags import chartit

        html = chartit.load_charts(None, 'my_chart')

        self.assertIn('<script type="text/javascript">', html)
        self.assertIn('var _chartit_hco_array = ();', html)
        self.assertIn('<script src="/static/chartit/js/chartloader.js" type="text/javascript">', html) # noqa

    @override_settings(CHARTIT_JS_REL_PATH='/chartit/js/')
    def test_setting_starting_with_slash(self):
        from chartit.templatetags import chartit

        html = chartit.load_charts(None, 'my_chart')

        self.assertIn('<script type="text/javascript">', html)
        self.assertIn('var _chartit_hco_array = ();', html)
        self.assertIn('<script src="/static/chartit/js/chartloader.js" type="text/javascript">', html) # noqa
