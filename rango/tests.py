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

from rango.decorators import chapter7
from rango.forms import CategoryForm, PageForm
from selenium.webdriver.chrome.options import Options

# ===== Chapter 7
class Chapter7LiveServerTestCase(StaticLiveServerTestCase):

    def setUp(self):
        from django.contrib.auth.models import User
        User.objects.create_superuser(username='admin', password='admin', email='admin@me.com')
        chrome_options = Options()        
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=800x600")        
        self.browser = webdriver.Chrome(chrome_options=chrome_options,executable_path=r'C:\chromedriver.exe')
        self.browser.implicitly_wait(3)

    @classmethod
    def setUpClass(cls):
        cls.host = socket.gethostbyname(socket.gethostname())
        super(Chapter7LiveServerTestCase, cls).setUpClass()

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    @chapter7
    def test_form_is_saving_new_category(self):
        # Access index page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('index'))

        # Check if is there link to add categories
        categories_link = self.browser.find_elements_by_partial_link_text('Add a New Category')
        if len(categories_link) == 0:
            categories_link = self.browser.find_elements_by_partial_link_text('Add New Category')

        categories_link[0].click()

        # Types new category name
        username_field = self.browser.find_element_by_name('name')
        username_field.send_keys('New Category')

        # Click on Create Category
        self.browser.find_element_by_css_selector(
            "input[type='submit']"
        ).click()

        body = self.browser.find_element_by_tag_name('body')

        # Check if New Category appears in the index page
        self.assertIn('New Category'.lower(), body.text.lower())

    @chapter7
    def test_form_error_when_category_field_empty(self):
        # Access index page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('index'))

        # Check if is there link to add categories
        categories_link = self.browser.find_elements_by_partial_link_text('Add a New Category')
        if len(categories_link) == 0:
            categories_link = self.browser.find_elements_by_partial_link_text('Add New Category')

        categories_link[0].click()

        url_path = self.browser.current_url
        response = self.client.get(url_path)

        self.assertIn('required'.lower(), response.content.lower())

    @chapter7
    def test_add_category_that_already_exists(self):
        # Create a category in database
        new_category = Category(name="New Category")
        new_category.save()

        # Access index page
        url = self.live_server_url
        url = url.replace('localhost', '127.0.0.1')
        self.browser.get(url + reverse('index'))

        # Check if is there link to add categories
        categories_link = self.browser.find_elements_by_partial_link_text('Add a New Category')
        if len(categories_link) == 0:
            categories_link = self.browser.find_elements_by_partial_link_text('Add New Category')

        categories_link[0].click()

        # Types new category name
        username_field = self.browser.find_element_by_name('name')
        username_field.send_keys('New Category')

        # Click on Create Category
        self.browser.find_element_by_css_selector(
            "input[type='submit']"
        ).click()

        body = self.browser.find_element_by_tag_name('body')

        # Check if there is an error message
        self.assertIn('Category with this Name already exists.'.lower(), body.text.lower())

    @chapter7
    def test_form_is_saving_new_page(self):
        #Create categories and pages
        categories = test_utils.create_categories()
        i = 0

        for category in categories:
            i = i + 1
            # Access link to add page for the category
            url = self.live_server_url
            url = url.replace('localhost', '127.0.0.1')
            self.browser.get(url + reverse('add_page', args=[category.slug]))

            # Types new page name
            username_field = self.browser.find_element_by_name('title')
            username_field.send_keys('New Page ' + str(i))

            # Types url for the page
            username_field = self.browser.find_element_by_name('url')
            username_field.send_keys('http://www.newpage1.com')

            # Click on Create Page
            self.browser.find_element_by_css_selector(
                "input[type='submit']"
            ).click()

            body = self.browser.find_element_by_tag_name('body')

            # Check if New Page appears in the category page
            self.assertIn('New Page'.lower(), body.text.lower())

    def test_cleaned_data_from_add_page(self):
        #Create categories and pages
        categories = test_utils.create_categories()
        i = 0

        for category in categories:
            i = i + 1
            # Access link to add page for the category
            url = self.live_server_url
            url = url.replace('localhost', '127.0.0.1')
            self.browser.get(url + '/rango/category/' + category.slug + '/add_page/')

            # Types new page name
            username_field = self.browser.find_element_by_name('title')
            username_field.send_keys('New Page ' + str(i))

            # Types url for the page
            username_field = self.browser.find_element_by_name('url')
            username_field.send_keys('http://www.newpage' + str(1) + '.com')

            # Click on Create Page
            self.browser.find_element_by_css_selector(
                "input[type='submit']"
            ).click()

            body = self.browser.find_element_by_tag_name('body')

            # Check if New Page appears in the category page
            self.assertIn('New Page'.lower(), body.text.lower())


class Chapter7ViewTests(TestCase):
    @chapter7
    def test_index_contains_link_to_add_category(self):
        # Access index
        try:
            response = self.client.get(reverse('index'))
        except:
            try:
                response = self.client.get(reverse('rango:index'))
            except:
                return False

        # Check if there is text and a link to add category
        self.assertIn('href="' + reverse('add_category') + '"', response.content.decode('ascii'))

    @chapter7
    def test_add_category_form_is_displayed_correctly(self):
        # Access add category page
        response = self.client.get(reverse('add_category'))

        # Check form in response context is instance of CategoryForm
        self.assertTrue(isinstance(response.context['form'], CategoryForm))

        # Check form is displayed correctly
        # Header
        self.assertIn('<h1>Add a Category</h1>'.lower(), response.content.decode('ascii').lower())

        # Label
        self.assertIn('Please enter the category name.'.lower(), response.content.decode('ascii').lower())

        # Text input
        self.assertIn('id="id_name"', response.content.decode('ascii'))
        self.assertIn('maxlength="128"', response.content.decode('ascii'))
        self.assertIn('name="name"', response.content.decode('ascii'))
        self.assertIn('type="text"', response.content.decode('ascii'))

        # Button
        self.assertIn('type="submit" name="submit" value="Create Category"'.lower(), response.content.decode('ascii').lower())

    @chapter7
    def test_add_page_form_is_displayed_correctly(self):
        # Create categories
        categories = test_utils.create_categories()

        for category in categories:
            # Access add category page
            try:
                response = self.client.get(reverse('index'))
                response = self.client.get(reverse('add_page', args=[category.slug]))
            except:
                try:
                    response = self.client.get(reverse('rango:index'))
                    response = self.client.get(reverse('rango:add_page', args=[category.slug]))
                except:
                    return False

            # Check form in response context is instance of CategoryForm
            self.assertTrue(isinstance(response.context['form'], PageForm))

            # Check form is displayed correctly

            # Label 1
            self.assertIn('Please enter the title of the page.'.lower(), response.content.decode('ascii').lower())

            # Label 2
            self.assertIn('Please enter the URL of the page.'.lower(), response.content.decode('ascii').lower())

            # Text input 1
            self.assertIn('id="id_title"'.lower(), response.content.decode('ascii').lower())
            self.assertIn('maxlength="128"'.lower(), response.content.decode('ascii').lower())
            self.assertIn('name="title"'.lower(), response.content.decode('ascii').lower())
            self.assertIn('type="text"'.lower(), response.content.decode('ascii').lower())

            # Text input 2
            self.assertIn('id="id_url"'.lower(), response.content.decode('ascii').lower())
            self.assertIn('maxlength="200"'.lower(), response.content.decode('ascii').lower())
            self.assertIn('name="url"'.lower(), response.content.decode('ascii').lower())
            self.assertIn('type="url"'.lower(), response.content.decode('ascii').lower())

            # Button
            self.assertIn('type="submit" name="submit" value="Add Page"'.lower(), response.content.decode('ascii').lower())

    def test_access_category_that_does_not_exists(self):
        # Access a category that does not exist
        response = self.client.get(reverse('show_category', args=['python']))

        # Check that it has a response as status code OK is 200
        self.assertEquals(response.status_code, 200)

        # Check the rendered page is not empty, thus it was customised (I suppose)
        self.assertNotEquals(response.content.decode('ascii'), '')

    def test_link_to_add_page_only_appears_in_valid_categories(self):
        # Access a category that does not exist
        response = self.client.get(reverse('show_category', args=['python']))

        # Check that there is not a link to add page
        try:
            self.assertNotIn(reverse('add_page', args=['python']), response.content.decode('ascii'))
            # Access a category that does not exist
            response = self.client.get(reverse('show_category', args=['other-frameworks']))
            # Check that there is not a link to add page
            self.assertNotIn(reverse('add_page', args=['other-frameworks']), response.content.decode('ascii'))
        except:
            try:
                self.assertNotIn(reverse('rango:add_page', args=['python']), response.content.decode('ascii'))
                # Access a category that does not exist
                response = self.client.get(reverse('rango:show_category', args=['other-frameworks']))
                # Check that there is not a link to add page
                self.assertNotIn(reverse('rango:add_page', args=['other-frameworks']), response.content.decode('ascii'))
            except:
                return False

    @chapter7
    def test_category_contains_link_to_add_page(self):
        # Crete categories
        categories = test_utils.create_categories()

        # For each category in the database check if contains link to add page
        for category in categories:
            try:
                response = self.client.get(reverse('show_category', args=[category.slug]))
                self.assertIn(reverse('add_page', args=[category.slug]), response.content.decode('ascii'))
            except:
                try:
                    response = self.client.get(reverse('rango:show_category', args=[category.slug]))
                    self.assertIn(reverse('rango:add_page', args=[category.slug]), response.content.decode('ascii'))
                except:
                    return False
