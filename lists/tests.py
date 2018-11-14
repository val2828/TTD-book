from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item, List
# Create your tests here.

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_uses_home_template(self):
        """ 
       The version of code without using the Test Client
       # Django sees the request object
        request = HttpRequest()
        # The request object is passed to home_page view
        response = home_page(request)
        # what is actually sent - extracted content of the response.
        html = response.content.decode('utf8')
        # ensure the sent string starts and ends with the html tags
        expected_html = render_to_string('home.html')
        # ensure that somewhere in the sent html there is a title
        # which says "To-Do lists" 
        self.assertEqual(html, expected_html)"""

        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        

class ListAndItemModelTest(TestCase):    
    
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response =self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

class NewListTest(TestCase):
    
    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={'item_text' : 'A new list item'})
        
        self.assertEqual (Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text' : 'A new list item'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')