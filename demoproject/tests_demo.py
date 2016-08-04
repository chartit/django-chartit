from demoproject.urls import urlpatterns
from django.test import Client, TestCase


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
