from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest (LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e 
                time.sleep(0.1)

    def test_can_start_a_list_for_one_user(self):
        # Customer visits the web-stites homepage
        self.browser.get(self.live_server_url)
    
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
        
        inputbox.send_keys('Buy peacock feathers')
        # Upon hitting Enter the page is updated and now the lists "1 : customer-input
        # input text " as an item in the To-Do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        
        # There is another text box whih invites to add another item. 
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        
        # Another update occurs
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        # A unique URL is generated for the customer with some reference text to it

        # Customer visits the URL and sees his list in-tact
        self.fail('Finish the test!')

        # table is updated and now shows both items she has put there
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # A new list is started
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        #Customer notices that the list has a unique url
        customer1_list_url = self.browser.current_url
        self.assertRegex(customer1_list_url, '/lists/.+')
        
        # Now a new user comes along to the site

        ## We use a new browser session to make sure that no information of the first user is coming through from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # The new user visits the home page and there is no trace of the list from the previous user
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text 
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # The new user starts a new list by entering a new item - shopping list

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # the new users gets his own unique url
        customer2_list_url = self.browser.current_url
        self.assertRegex(customer2_list_url, '/lists/.+')
        self.assertNotEqual(customer1_list_url, customer2_list_url)

        # again, there is no trace of the first user's list
        page_text = self.browser.find_element_by_tag_name('body').text 
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
        print(page_text)