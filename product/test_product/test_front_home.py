import os
import time

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from django.test import TestCase
import pytest
from selenium import webdriver


# from .models import Album, Artist, Contact, Booking



# driver.get('http://www.google.com/')
# time.sleep(5) # Let the user actually see something!
# search_box = driver.find_element_by_name('q')
# search_box.send_keys('ChromeDriver')
# search_box.submit()
# time.sleep(5) # Let the user actually see something!
# driver.quit()


# Front Anomymous
class TestHomeAnomymous(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # cls.USER_EMAIL = 'user@dummy.com'
        # cls.USER_NAME = cls.USER_EMAIL
        # cls.USER_PWD = 'dummy_pwd'
        
        # cls.KNOWN_EMAIL = 'known_user@dummy.com'
        # cls.KNOWN_NAME = cls.KNOWN_EMAIL
        # cls.KNOWN_PWD = 'dummy_known_pwd'
        # user = get_user_model().objects.create_user(cls.KNOWN_NAME, cls.KNOWN_EMAIL, cls.KNOWN_PWD)
        # print('Dummy known user {} is created for test: {}'.format(user, user != None))


        cls.HOST = 'http://127.0.0.1:8000'
        
    def setUp(self):
        base = os.path.dirname(settings.BASE_DIR)
        driver = webdriver.Chrome(executable_path=os.path.join(base, 'chromedriver.exe'))  # Optional argument, if not specified will search path.
        # driver = webdriver.Firefox(os.path.join(base, 'geckodriver.exe'))
        # with webdriver.Chrome(executable_path=os.path.join(base, 'chromedriver.exe')) as driver:
        self.WEB_DRIVER = driver
        self.WEB_DRIVER.get(self.HOST)
        time.sleep(3)

    def tearDown(self):
        self.client.logout()
        self.WEB_DRIVER.quit()
        time.sleep(3)

    def test_home_2_notice_page(self):
        """
        test that notice page returns a 200
        """
        driver = self.WEB_DRIVER

        # notice_link = driver.find_element_by_id('notice_lnk')
        notice_link = driver.find_element_by_partial_link_text('Mention')

        time.sleep(3)
        notice_link.click()
        time.sleep(3)

        # response = self.client.get(reverse('account:signup'))
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(driver.current_url, self.HOST + reverse('product:notice'))

    def test_home_2_contact_section(self):
        """
        test that notice page returns a 200
        """
        driver = self.WEB_DRIVER
        driver.get(self.HOST + reverse('product:notice'))
        time.sleep(3)

        contact_link = driver.find_element_by_id('contact_lnk')
        # contact_link = driver.find_element_by_partial_link_text('Contact')
        time.sleep(3)

        contact_link.click()
        time.sleep(3)

        # response = self.client.get(reverse('account:signup'))
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(driver.current_url, self.HOST + '/#contact')


# # Front Authenticated
# class TestFrontAuthenticated(TestCase):
    
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

