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

# from .models import Album, Artist, Contact, Booking

DEFAULT_TIMEOUT_S = 7
SEARCH_TIMEOUT_S = 180
DISABLE_TEST = True


# Tests of Front for anomymous product pages
class TestFrontProductAnomymous(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):

        super().setUpClass()

        # Create driver
        base = os.path.dirname(settings.BASE_DIR)
        cls.WEB_DRIVER = webdriver.Chrome(executable_path=os.path.join(base, 'chromedriver.exe'))
        cls.WEB_DRIVER.maximize_window()

    @classmethod
    def tearDownClass(cls):

        # Close driver
        # cls.WEB_DRIVER.close()
        cls.WEB_DRIVER.quit()   # Warning: Quit webdriver but generate exception
        super().tearDownClass()


    def setUp(self):
        # self.WEB_DRIVER.get(self.live_server_url)
        # self.addCleanup(self.WEB_DRIVER.quit)
        pass
        
    def tearDown(self):
        pass


    def test_front_result(self):
        """
        Test that Result page returns a 200
        """

        # data = {
        #     'user_query': 'kinder bueno',
        # }
        response = self.client.get(reverse('product:result', args=['kinder bueno'])) # kwargs=data
        self.assertEqual(response.status_code, 200)

    @unittest.skipIf(DISABLE_TEST, "[TODO]")
    def test_front_favorite(self):
        """
        Test that Favorite page redirects to Sign-in page
        """
        response = self.client.get(reverse('product:favorite'), follow=True)
        self.assertContains(response, reverse('account:signin'))
        self.assertEqual(response.status_code, 200)

    # def test_front_parse_favorite_page(self):
    #     """
    #     test that index page returns a 200
    #     """
    #     response = self.client.get(reverse('product:parse_favorite'))
    #     self.assertEqual(response.status_code, 200)

    # def test_front_info_page(self):
    #     """
    #     test that index page returns a 200
    #     """
    #     response = self.client.get(reverse('product:home'))
    #     self.assertEqual(response.status_code, 200)

# Tests of Front for authenticated product pages
class TestFrontProductAuthenticated(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):

        super().setUpClass()

        # Create user
        cls.USER_PWD = 'dummy_pwd'
        email = 'user@dummy.com'
        username = email

        cls.USER = get_user_model().objects.create_user(username, email, cls.USER_PWD)

        # # Create driver
        base = os.path.dirname(settings.BASE_DIR)
        cls.WEB_DRIVER = webdriver.Chrome(executable_path=os.path.join(base, 'chromedriver.exe'))
        cls.WEB_DRIVER.maximize_window()


    @classmethod
    def tearDownClass(cls):

        # # Close driver
        # cls.WEB_DRIVER.close()
        cls.WEB_DRIVER.quit()   # Warning: Quit webdriver but generate exception
        time.sleep(3)
        super().tearDownClass()


    def setUp(self):

        # sign-in user
        # print('COOKIE_X', self.client.cookies, 'THERE_IS_X', self.client.session, 'OFF_X')
        # time.sleep(7)

        self.client.login(username=self.USER.username, password=self.USER_PWD)
        # [TODO] Check doc or forum to understand why it is mandatory to load session
        self.client.session
        self.client.cookies
        # print('COOKIE_Y', self.client.cookies, 'THERE_IS_Y', self.client.session, 'OFF_Y')

        # share session to webdriver
        cookie = self.client.cookies['sessionid']
        # print('CKKKKKKKKKKKKKKKKKKKKKKIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII', cookie)

        self.WEB_DRIVER.get(self.live_server_url)
        # print('RRRRREEEEEEEEEEELLLLLLLLLLLLLOOOOOOOOOOOAAAAAAAAAADDDDDDDDDDDDDD')
        # time.sleep(7)

        self.WEB_DRIVER.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})  # , 'Domain': self.live_server_url
        # print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADDDDDDDDDDDDDD')
        # time.sleep(7)
        self.WEB_DRIVER.refresh()
        # print('FFFFFFFFFFFFFFFFFFFFFFFFFFFRRRRRRRRRRRRRRRRRRRREEEEEEEEEEEEEEEESSSS')
        # time.sleep(7)
        # self.addCleanup(self.WEB_DRIVER.quit)

    def tearDown(self):
        # self.WEB_DRIVER.delete_cookie('sessionid')
        # self.client.logout()
        pass


    # def test_front_result(self):
    #     """
    #     Test that Result page returns a 200
    #     """
    #     data = {
    #         'user_query': 'prince',
    #     }
    #     response = self.client.get(reverse('product:result', kwargs=data))
    #     self.assertEqual(response.status_code, 200)

    # def test_front_favorite(self):
    #     """
    #     Test that Favorite page return 200
    #     """
    #     response = self.client.get(reverse('product:favorite'))
    #     self.assertEqual(response.status_code, 200)

    def test_front_parse_favorite_page(self):
        """
        test that index page returns a 200
        """
        # data = {
        #     'user_query': 'oreo',
        # }
        driver = self.WEB_DRIVER
        query = "oreo"

        # Set the query and send by Enter key pressed
        nav = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(EC.visibility_of_element_located((By.ID, 'navbarResponsive')))
        # nav = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('navbarResponsive'))
        nav.find_element_by_name("query").send_keys(query+Keys.ENTER)
        product_section = WebDriverWait(driver, SEARCH_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('product_section'))

        self.assertEqual(driver.current_url, self.live_server_url + reverse('product:result', args=[query]))

        # product_section = WebDriverWait(driver, SEARCH_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('product_section'))

        favorite_link_lst = product_section.find_elements_by_tag_name('a')
        product_id_lst = []
        for favorite in favorite_link_lst:
            product_id_lst.append(int(favorite.get_attribute("id")))
            print('ID', product_id_lst[-1], product_id_lst[-1] % 2)
            favorite.click()
            time.sleep(3)
            if not product_id_lst[-1] % 2:
                favorite_link = product_section.find_element_by_id(str(product_id_lst[-1]))
                favorite_link.click()
                time.sleep(3)

        # self.assertEqual(response.status_code, 200)

    # def test_front_info_page(self):
    #     """
    #     test that index page returns a 200
    #     """
    #     response = self.client.get(reverse('product:home'))
    #     self.assertEqual(response.status_code, 200)


# Tests of Front for authenticated product pages
class TestFrontProductAuthenticatedMisc(TestCase):

    @classmethod
    def setUpClass(cls):

        super().setUpClass()

        # Create user
        cls.USER_PWD = 'dummy_pwd'
        email = 'user@dummy.com'
        username = email

        cls.USER = get_user_model().objects.create_user(username, email, cls.USER_PWD)

    @classmethod
    def tearDownClass(cls):

        super().tearDownClass()


    def setUp(self):

        # sign-in user
        self.client.login(username=self.USER.username, password=self.USER_PWD)
        # [TODO] Check doc or forum to understand why it is mandatory to load session
        self.client.session
        self.client.cookies

    def tearDown(self):
        # self.client.logout()
        pass


    def test_front_result(self):
        """
        Test that Result page returns a 200
        """
        data = {
            'user_query': 'prince',
        }
        response = self.client.get(reverse('product:result', kwargs=data))
        self.assertEqual(response.status_code, 200)

    def test_front_favorite(self):
        """
        Test that Favorite page return 200
        """
        response = self.client.get(reverse('product:favorite'))
        self.assertEqual(response.status_code, 200)










#     @pytest.mark.django_db(transaction=False)
#     def test_my_user():
#         me = User.objects.get(username='me')
#         assert me.is_superuser



# # Detail Page
# class DetailPageTestCase(TestCase):

#     def setUp(self):
#         # ran before each test.
    
#         impossible = Album.objects.create(title="Transmission Impossible")
#         self.album = Album.objects.get(title='Transmission Impossible')


# # Booking Page
# class BookingPageTestCase(TestCase):
    
#     def setUp(self):
#         Contact.objects.create(name="Freddie", email="fred@queen.forever")
#         impossible = Album.objects.create(title="Transmission Impossible")
#         journey = Artist.objects.create(name="Journey")
#         impossible.artists.add(journey)
#         self.album = Album.objects.get(title='Transmission Impossible')
#         self.contact = Contact.objects.get(name='Freddie')


#     def test_new_booking_is_registered(self):
#         # test that a new booking is made

#         old_bookings = Booking.objects.count() # count bookings before a request

#         album_id = self.album.id
#         name = self.contact.name
#         email =  self.contact.email
        
#         response = self.client.post(reverse('store:detail', args=(album_id,)), {
#             'name': name,
#             'email': email
#         })

#         new_bookings = Booking.objects.count() # count bookings after
#         self.assertEqual(new_bookings, old_bookings + 1) # make sure 1 booking was added
