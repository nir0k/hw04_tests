from django.test import TestCase, Client
from django.core.cache import cache


class ViewTestClass(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def tearDown(self):
        cache.clear()

    def test_error_page(self):
        response = self.guest_client.get('/nonexist-page/')
        self.assertTemplateUsed(response, 'core/404.html')
