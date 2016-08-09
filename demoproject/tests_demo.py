from chartit import DataPool, Chart
from django.core.cache import cache
from demoproject.urls import urlpatterns
from django.test import Client, TestCase
from demoproject.models import SalesHistory, BookStore


class DemoProject_TestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_all_views_load(self):
        """
            A simple sanity test to make sure all views from demoproject
            still continue to load!
        """
        for url in urlpatterns:
            address = url._regex
            if address.startswith('^'):
                address = '/' + address[1:]
            if address.endswith('$'):
                address = address[:-1]
            response = self.client.get(address)
            self.assertEqual(response.status_code, 200)


class DjangoCache_TestCase(TestCase):
    def setUp(self):
        ds = DataPool(
                series=[{
                    'options': {
                        'source': SalesHistory.objects.filter(
                                            bookstore=BookStore.objects.first()
                                  )[:10]
                    },
                    'terms': ['sale_date', 'sale_qty']
                }]
        )

        self.chart = Chart(
                datasource=ds,
                series_options=[{
                    'options': {
                        'type': 'line',
                        'stacking': False
                    },
                    'terms': {
                        'sale_date': ['sale_qty']
                    }
                }],
                chart_options={
                    'title': {'text': 'Sales QTY per day'},
                    'xAxis': {'title': {'text': 'Sale date'}}
                }
        )

    def test_cache_set_cache_get(self):
        cache.set('my-chart', self.chart, 30)
        chart = cache.get('my-chart')
        self.assertIsNotNone(chart)
