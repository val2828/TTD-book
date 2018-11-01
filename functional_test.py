from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

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
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Customer is invited to make a list right away
        # There is a text box that the customer can feel in
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        
        inputbox.send_keys('Buy peackock feathers')
        # Upon hitting Enter the page is updated and now the lists "1 : customer-input
        # input text " as an item in the To-Do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1000)
        
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peackock feathers' for row in rows),
            "New to-do item did not appear in table"
        )
        # There is another text box whih invites to add another item. 
        self.fail('Finish the test!')
        # Another update occurs

        # A unique URL is generated for the customer with some reference text to it

        # Customer visits the URL and sees his list in-tact


if __name__ == '__main__':
    unittest.main(warnings='ignore')
