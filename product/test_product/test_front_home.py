import os
import time


from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

import unittest
from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from django.test.utils import setup_test_environment
import pytest
from selenium import webdriver
# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


DEFAULT_TIMEOUT_S = 12
SEARCH_TIMEOUT_S = 180
DISABLE_TEST = True


# Front Base and Home Anomymous
class TestFrontHomeAnomymous(StaticLiveServerTestCase):
    
    # fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):

        super().setUpClass()

        # Create driver
        cls.WEB_DRIVER = create_webdriver()
        cls.WEB_DRIVER.maximize_window()
        

    @classmethod
    def tearDownClass(cls):

        # Close driver
        # cls.WEB_DRIVER.close()
        cls.WEB_DRIVER.quit()   # Warning: Quit webdre=iver but generate exception
        super().tearDownClass()


    def setUp(self):
        self.WEB_DRIVER.get(self.live_server_url)
        # self.addCleanup(self.WEB_DRIVER.quit)
        
    def tearDown(self):
        pass


    def test_home_page(self):
        """
        Check Home page returns a 200
        """
        response = self.client.get(reverse('product:home'))
        self.assertEqual(response.status_code, 200)


    def test_website_title(self):
        """
        Check Website title
        """
        self.assertEqual("Pur Beurre", self.WEB_DRIVER.title)

    # --- Header ---
    def test_other_2_home(self):
        """
        Check navigation to Home page
        """
        driver = self.WEB_DRIVER

        # Go to another page
        driver.get(build_full_url(self, 'product:notice'))
        WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('notice_section_id'))

        # Go to Home page
        home_link = driver.find_element_by_id('zlogo')
        # contact_link = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(
        #                                     EC.element_to_be_clickable((By.ID, 'zlogo')))
        home_link.click()
        WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('history'))

        self.assertEqual(driver.current_url[:-1], self.live_server_url)

    @unittest.skipIf(DISABLE_TEST, "ERROR:Random timeout by using WebDriverWait")
    def test_home_2_signin_page(self):
        """
        Check navigation from Home to Sign-in page
        """
        driver = self.WEB_DRIVER

        # Go to Sign-in page
        # singin_link = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(EC.element_to_be_clickable((By.ID, 'signin_a')))
        WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('signin_a'))

        singin_link = driver.find_element_by_id('signin_a')
        singin_link.click()
        WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('contact'))

        self.assertEqual(driver.current_url, self.live_server_url + '/#contact')

    def test_nav_search_bar_2_result_page(self):
        """
        Check navigation from search bar to product result page
        """
        driver = self.WEB_DRIVER
        query = "nutella"

        # Set the query and send by Enter key pressed
        nav = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(EC.visibility_of_element_located((By.ID, 'navbarResponsive')))
        # nav = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('navbarResponsive'))
        nav.find_element_by_name("query").send_keys(query+Keys.ENTER)
        WebDriverWait(driver, SEARCH_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('product_section'))

        self.assertEqual(driver.current_url, build_full_url(self, 'product:result', {'user_query':query}))

    @unittest.skipIf(DISABLE_TEST, "ERROR:server error occurs")
    def test_nav_search_bar_2_result_page_button(self):
        """
        Check navigation from search bar to product result page
        """
        driver = self.WEB_DRIVER
        query = "oreo"

        # Set the query
        nav = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(EC.visibility_of_element_located((By.ID, 'navbarResponsive')))
        nav.find_element_by_name("query").send_keys(query)

        # Send the query by clicking the search button
        nav.find_element_by_css_selector("button[type='submit']").click()
        WebDriverWait(driver, SEARCH_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('product_section'))

        self.assertEqual(driver.current_url, build_full_url(self, 'product:result', {'user_query':query}))

    # --- Home search bar ---
    # @unittest.skipIf(DISABLE_TEST, "ERROR:server error occurs")
    def test_home_search_bar_2_result_page(self):
        """
        Check navigation from search bar to product result page
        """
        driver = self.WEB_DRIVER
        query = "twix"

        # Set the query
        masthead = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(EC.visibility_of_element_located((By.CLASS_NAME, 'masthead')))
        masthead.find_element_by_name("query").send_keys(query)

        # Send the query by clicking the search button
        masthead.find_element_by_css_selector("button[type='submit']").click()

        WebDriverWait(driver, SEARCH_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('product_section'))

        self.assertEqual(driver.current_url, build_full_url(self, 'product:result', {'user_query':query}))

    # --- Footer ---
    @unittest.skipIf(DISABLE_TEST, "ERROR:Random timeout by using WebDriverWait")
    def test_home_2_notice_page(self):
        """
        Check navigation from Home to Notices page
        """
        driver = self.WEB_DRIVER

        # Go to Notice page
        # WebDriverWait(driver, DEFAULT_TIMEOUT).until(lambda d: d.find_element_by_id('notice_a'))
        notice_link = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(EC.element_to_be_clickable((By.ID, 'notice_a')))
        # print('NOTICE_LINK', notice_link)
        notice_link.click()
        time.sleep(1)
        
        # notice_link = driver.find_element_by_partial_link_text('Mention')
        # driver.find_element_by_id('notice_a').click()
        # notice_link = driver.find_element_by_id('notice_a')
        # print('NOTICE_LINK', notice_link)
        # notice_link.click()
        WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('notice_section_id'))

        self.assertEqual(driver.current_url, build_full_url(self, 'product:notice'))

    def test_other_2_contact_section(self):
        """
        Check navigation to Home:Contact section
        """
        driver = self.WEB_DRIVER

        # Go to another page
        driver.get(build_full_url(self, 'product:notice'))
        WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('notice_section_id'))

        # Go to Home/Contact section
        contact_link = driver.find_element_by_id('contact_lnk')
        # contact_link = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(
        #                                     EC.element_to_be_clickable((By.ID, 'contact_lnk')))
        contact_link.click()
        WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('contact'))

        self.assertEqual(driver.current_url, self.live_server_url + '/#contact')


# Front Base and Home Authenticated
class TestFrontHomeAuthenticated(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):

        super().setUpClass()
        
        # Create user
        cls.USER, cls.USER_PWD = create_user()

        # Create driver
        cls.WEB_DRIVER = create_webdriver()
        cls.WEB_DRIVER.maximize_window()

    @classmethod
    def tearDownClass(cls):

        # Close driver
        # cls.WEB_DRIVER.close()
        cls.WEB_DRIVER.quit()   # Warning: Quit webdriver but generate exception
        time.sleep(3)
        super().tearDownClass()


    def setUp(self):
        
        print('CLIENT_B', self.client, 'OUT')
        print('SESSION', self.client.session)
        print('COOKIES', self.client.cookies)

        # Sign-in user
        sign_in_user_into_webdriver(self, self.USER, self.USER_PWD, self.WEB_DRIVER, 'product:home')

    def tearDown(self):
        # self.WEB_DRIVER.delete_cookie('sessionid')
        # self.client.logout()
        pass

    @unittest.skipIf(DISABLE_TEST, "ERROR:Random timeout by using WebDriverWait")
    def test_home_to_profil(self):
        """
        Check navigation from Home to Profile page
        """
        driver = self.WEB_DRIVER

        # Go to Profile
        profile_link = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(
                                            EC.element_to_be_clickable((By.ID, 'profile_a')))
        profile_link.click()
        time.sleep(1)
        WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('profile_section_id'))

        self.assertEqual(driver.current_url, build_full_url(self, 'account:profile'))


    @unittest.skipIf(DISABLE_TEST, "ERROR:Random timeout by using WebDriverWait")
    def test_home_to_favorite(self):
        """
        Check navigation from Home to Favorite page
        """
        driver = self.WEB_DRIVER

        # Go to Profile
        favorite_link = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(
                                            EC.element_to_be_clickable((By.ID, 'favorite_a')))
        favorite_link.click()
        time.sleep(1)
        WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('product_section'))

        self.assertEqual(driver.current_url, build_full_url(self, 'product:favorite'))


class TestFrontMisc(TestCase):
    
    @classmethod
    def setUpTestData(cls):

        # cls.csrf_client = Client(enforce_csrf_checks=True, json_encoder=DjangoJSONEncoder, HTTP_USER_AGENT='Mozilla/5.0', **defaults)
        pass
        
    @classmethod
    def tearDownTestData(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_notice_page(self):
        """
        Test that Notice page returns a 200
        """
        response = self.client.get(reverse('product:notice'))
        self.assertEqual(response.status_code, 200)

    def test_contact_section(self):
        """
        test that contact section returns a 200
        """
        url = reverse('product:home') + '#contact'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


# elem = browser.find_element_by_name('p')  # Find the search box
# elem.send_keys('seleniumhq' + Keys.RETURN)

# search_box = driver.find_element_by_name('q')
# search_box.send_keys('ChromeDriver')
# search_box.submit()


def create_webdriver():
    """
    Create browser webdriver
    """
    # base = os.path.dirname(settings.BASE_DIR)
    base = os.path.dirname('~/virtualenv/python3.6/bin/chromedriver' )
    # with webdriver.Chrome(executable_path=os.path.join(base, 'chromedriver.exe')) as driver:
    driver = webdriver.Chrome(executable_path=os.path.join(base, 'chromedriver'))
    # driver.implicitly_wait(10)
    # time.sleep(1)

    return driver

def build_full_url(obj, relative_url_name, kwargs=None):
    """
    Build full url from domain root and with specified reltive part
    """
    return obj.live_server_url + reverse(relative_url_name, kwargs=kwargs)

def create_user():
    """
    Create a dummy user
    """

    pwd = 'dummy_pwd'
    email = 'user@dummy.com'
    username = email
    user = get_user_model().objects.create_user(username, email, pwd)
    # print('Dummy user {} is created for test: {}'.format(user, user != None))

    return user, pwd

def sign_in_user_into_webdriver(obj, user, password, driver, relative_url):

    print('COOKIE_X', obj.client.cookies, 'THERE_IS_X', obj.client.session, 'OFF_X')
    # sign-in user
    obj.client.login(username=user.username, password=password)

    # share session to webdriver
    # [TODO] Check doc or forum to understand why it is mandatory to load session
    print('COOKIE_A', obj.client.cookies, 'THERE_IS', obj.client.session, 'OFF')
    cookie = obj.client.cookies['sessionid']
    print('COOKIE_B', cookie)
    driver.get(build_full_url(obj, relative_url))  #selenium will set cookie domain based on current page domain
    driver.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
    driver.refresh() #need to update page for logged in user
