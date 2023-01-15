from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()       
        self.urls_templates = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }

    def test_url(self):
        for url in self.urls_templates.keys():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_url_template(self):
        for url, template in self.urls_templates.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
