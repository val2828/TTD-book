from selenium import webdriver
import unittest

class NewVisitorTest (unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Customer visits the web-stites homepage
        self.browser.get('http://localhost:8000')
    
        # Notice the header to contain term To-Do
        self.assertIn('To-Do', self.browser.title)
        self.fail ('Finish the test!')

        # Customer is invited to make a list right away

        # There is a text box that the customer can feel in

        # Upon hitting Enter the page is updated and now the lists "1 : customer-input
        # input text " as an item in the To-Do list

        # There is another text box whih invites to add another item. 

        # Another update occurs

        # A unique URL is generated for the customer with some reference text to it

        # Customer visits the URL and sees his list in-tact

if __name__ == '__main__':
    unittest.main(warnings='ignore')
