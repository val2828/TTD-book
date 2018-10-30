from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page
# Create your tests here.

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        # Django sees the request object
        request = HttpRequest()
        # The request object is passed to home_page view
        response = home_page(request)
        # what is actually sent - extracted content of the response.
        html = response.content.decode('utf8')
        # ensure the sent string starts and ends with the html tags
        self.assertTrue(html.startswith('<html>'))
        # ensure that somewhere in the sent html there is a title
        # which says "To-Do lists" 
        self.assertIn('<title>To-Do lists</title>',html)
        self.assertTrue(html.endswith('</html>'))