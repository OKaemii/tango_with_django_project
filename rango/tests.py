# Chapter 3
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.core.urlresolvers import reverse
import os
import socket
from selenium.webdriver.chrome.options import Options


# ===== CHAPTER 3
class Chapter3LiveServerTests(StaticLiveServerTestCase):

    def setUp(self):
        chrome_options = Options()        
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=800x600")        
        self.browser = webdriver.Chrome(chrome_options=chrome_options,executable_path=r'C:\chromedriver.exe')
        self.browser.implicitly_wait(3)

    @classmethod
    def setUpClass(cls):
        cls.host = socket.gethostbyname(socket.gethostname())
        super(Chapter3LiveServerTests, cls).setUpClass()

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()        

    def test_navigate_from_index_to_about(self):
        # Go to rango main page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('index'))

        # Search for a link to About page
        about_link = self.browser.find_element_by_partial_link_text("About")
        about_link.click()

        # Check if it goes back to the home page
        self.assertIn(url + reverse('about'), self.browser.current_url)

    def test_navigate_from_about_to_index(self):
        # Go to rango main page
        self.client.get(reverse('index'))
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('about'))

        # Check if there is a link back to the home page
        # link_to_home_page = self.browser.find_element_by_tag_name('a')
        link_to_home_page = self.browser.find_element_by_link_text('Index')
        link_to_home_page.click()

        # Check if it goes back to the home page
        self.assertEqual(url + reverse('index'), self.browser.current_url)        


class Chapter3ViewTests(TestCase):
    def test_index_contains_hello_message(self):
        # Check if there is the message 'hello world!'
        response = self.client.get(reverse('index'))
        self.assertIn('Rango says'.lower(), response.content.decode('ascii').lower())

        # file.write('test_index_contains_hello_message\n')

    def test_about_contains_create_message(self):
        # Check if in the about page is there a message
        self.client.get(reverse('index'))
        response = self.client.get(reverse('about'))
        self.assertIn('Rango says here is the about page'.lower(), response.content.decode('ascii').lower())

# ===== CHAPTER 4
class Chapter4ViewTest(TestCase):

    def test_view_has_title(self):
        response = self.client.get(reverse('index'))

        #Check title used correctly
        self.assertIn('<title>', response.content.decode('ascii'))
        self.assertIn('</title>', response.content.decode('ascii'))

    def test_index_using_template(self):
        response = self.client.get(reverse('index'))

        # Check the template used to render index page
        self.assertTemplateUsed(response, 'rango/index.html')

    def test_about_using_template(self):
        self.client.get(reverse('index'))
        response = self.client.get(reverse('about'))

        # Check the template used to render about page
        self.assertTemplateUsed(response, 'rango/about.html')

    def test_rango_picture_displayed(self):
        response = self.client.get(reverse('index'))

        # Check if is there an image in index page
        self.assertIn('img src="/static/images/rango.jpg'.lower(), response.content.decode('ascii').lower())

    # New media test
    def test_cat_picture_displayed(self):
        response = self.client.get(reverse('about'))

        # Check if is there an image in index page
        self.assertIn('img src="/media/cat.jpg'.lower(), response.content.decode('ascii').lower())

    def test_about_contain_image(self):
        self.client.get(reverse('index'))
        response = self.client.get(reverse('about'))

        # Check if is there an image in index page
        self.assertIn('img src="/static/images/', response.content.decode('ascii'))

    def test_serving_static_files(self):
        # If using static media properly result is not NONE once it finds rango.jpg
        result = finders.find('images/rango.jpg')
        self.assertIsNotNone(result)