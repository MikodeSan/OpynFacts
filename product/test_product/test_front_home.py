import os
import time


from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

import unittest
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from django.test.utils import setup_test_environment
import pytest
from selenium import webdriver
# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from .models import Album, Artist, Contact, Booking


DEFAULT_TIMEOUT_S = 7

# Front Home Anomymous
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


    def test_home_2_notice_page(self):
        """
        Check navigation from Home to Notices page
        """
        driver = self.WEB_DRIVER

        # Go to Notice page
        # WebDriverWait(driver, DEFAULT_TIMEOUT).until(lambda d: d.find_element_by_id('profile_a'))
        notice_link = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(EC.element_to_be_clickable((By.ID, 'notice_a')))
        # print('NOTICE_LINK', notice_link)
        notice_link.click()
        
        # notice_link = driver.find_element_by_partial_link_text('Mention')
        # driver.find_element_by_id('notice_a').click()
        # notice_link = driver.find_element_by_id('notice_a')
        # print('NOTICE_LINK', notice_link)
        # notice_link.click()
        WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('notice_section_id'))

        self.assertEqual(driver.current_url, build_full_url(self, 'product:notice'))


    def test_home_2_contact_section(self):
        """
        Check navigation to Home:Contact section
        """
        driver = self.WEB_DRIVER

        # Go to other page
        driver.get(build_full_url(self, 'product:notice'))
        WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('notice_section_id'))

        # Go to Home/Contact section
        contact_link = driver.find_element_by_id('contact_lnk')
        # contact_link = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(
        #                                     EC.element_to_be_clickable((By.ID, 'contact_lnk')))
        contact_link.click()
        WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('contact'))

        self.assertEqual(driver.current_url, self.live_server_url + '/#contact')


# Front Home Authenticated
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
        super().tearDownClass()


    def setUp(self):
        # self.client = Client()

        # Sign-in user
        sign_in_user_into_webdriver(self, self.USER, self.USER_PWD, self.WEB_DRIVER, 'product:home')

    def tearDown(self):
        self.WEB_DRIVER.delete_all_cookies()
        self.client.logout()


    def test_home_to_profil(self):
        """
        Check navigation from Home to Profile page
        """
        driver = self.WEB_DRIVER

        # Go to Profile
        contact_link = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(
                                            EC.element_to_be_clickable((By.ID, 'profile_a')))
        contact_link.click()
        # time.sleep(3)
        WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('profile_section_id'))

        self.assertEqual(driver.current_url, build_full_url(self, 'account:profile'))


    # def test_home_2_notice_page(self):
    #     """
    #     test navigation from home to notices page
    #     """
    #     driver = self.WEB_DRIVER

    #     # notice_link = driver.find_element_by_id('notice_lnk')
    #     notice_link = driver.find_element_by_partial_link_text('Mention')

    #     time.sleep(1)
    #     notice_link.click()
    #     time.sleep(1)

    #     # response = self.client.get(reverse('account:signup'))
    #     # self.assertEqual(response.status_code, 200)
    #     self.assertEqual(driver.current_url, self.HOST + reverse('product:notice'))


    
#     @classmethod
#     def setUpTestData(cls):
#         cls.USER_PWD = 'dummy_pwd'
#         email = 'user@dummy.com'
#         username = email
#         cls.USER = get_user_model().objects. create_user(username, email, cls.USER_PWD)
#         print('Dummy user {} is created for test: {}'.format(cls.USER, cls.USER != None))

#     def setUp(self):
#         # self.client = Client()
#         self.client.login(username=self.USER.username, password=self.USER_PWD)

#     def tearDown(self):
#         self.client.logout()

#     def test_front_signup_page(self):
#         """
#         [TODO] Test that sign-up page redirects to sign-out request page
#         """
#         pass


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
    base = os.path.dirname(settings.BASE_DIR)
    # with webdriver.Chrome(executable_path=os.path.join(base, 'chromedriver.exe')) as driver:
    driver = webdriver.Chrome(executable_path=os.path.join(base, 'chromedriver.exe'))
    # driver.implicitly_wait(10)
    # time.sleep(1)

    return driver

def build_full_url(obj, relative_url_name):
    """
    Build full url from domain root and with specified reltive part
    """
    return obj.live_server_url + reverse(relative_url_name)

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

    # sign-in user
    obj.client.login(username=user.username, password=password)

    # share session to webdriver
    cookie = obj.client.cookies['sessionid']
    driver.get(build_full_url(obj, relative_url))  #selenium will set cookie domain based on current page domain
    driver.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
    driver.refresh() #need to update page for logged in user
