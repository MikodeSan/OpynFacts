import os
import sys

base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base)

from test_util import *


# Tests of Front for anomymous product pages
class TestFrontProductAnomymous(StaticLiveServerTestCase):
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
        cls.WEB_DRIVER.quit()  # Warning: Quit webdriver but generate exception
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
        response = self.client.post(
            reverse("product:result", args=["kinder bueno"])
        )  # kwargs=data
        self.assertEqual(response.status_code, 200)

    @unittest.skipIf(DISABLE_TEST, "[TODO]")
    def test_front_favorite(self):
        """
        Test that Favorite page redirects to Sign-in page
        """
        response = self.client.get(reverse("product:favorite"), follow=True)
        self.assertContains(response, reverse("account:signin"))
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
        cls.USER_PWD = "dummy_pwd"
        email = "user@dummy.com"
        username = email

        cls.USER = get_user_model().objects.create_user(username, email, cls.USER_PWD)

        # # Create driver
        cls.WEB_DRIVER = create_webdriver()
        cls.WEB_DRIVER.maximize_window()

    @classmethod
    def tearDownClass(cls):

        # # Close driver
        # cls.WEB_DRIVER.close()
        cls.WEB_DRIVER.quit()  # Warning: Quit webdriver but generate exception
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
        cookie = self.client.cookies["sessionid"]
        # print('CKKKKKKKKKKKKKKKKKKKKKKIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII', cookie)

        self.WEB_DRIVER.get(self.live_server_url)
        # print('RRRRREEEEEEEEEEELLLLLLLLLLLLLOOOOOOOOOOOAAAAAAAAAADDDDDDDDDDDDDD')
        # time.sleep(7)

        self.WEB_DRIVER.add_cookie(
            {"name": "sessionid", "value": cookie.value, "secure": False, "path": "/"}
        )  # , 'Domain': self.live_server_url
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

    @unittest.skipIf(DISABLE_TEST, "ERROR:Random timeout by using WebDriverWait")
    def test_front_parse_favorite_page(self):
        """
        Test that favorite product can be set and then Go to product information page
        """
        # data = {
        #     'user_query': 'oreo',
        # }
        driver = self.WEB_DRIVER
        query = "oreo"

        # --- Go to Result page ---

        # Set the query and send by Enter key pressed
        nav = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(
            EC.visibility_of_element_located((By.ID, "navbarResponsive"))
        )
        # nav = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('navbarResponsive'))
        nav.find_element_by_name("query").send_keys(query + Keys.ENTER)
        product_section = WebDriverWait(driver, SEARCH_TIMEOUT_S).until(
            lambda drv: drv.find_element_by_id("product_section")
        )

        self.assertEqual(
            driver.current_url,
            self.live_server_url + reverse("product:result", args=[query]),
        )

        # --- Targeted product ---
        masthead = driver.find_element_by_class_name("masthead")
        link_lst = masthead.find_elements_by_tag_name("a")

        # Set targeted product as favorite
        link_itr = iter(link_lst)
        enable = True
        while enable:

            try:
                link = next(link_itr)

                if link.get_attribute(
                    "data-state"
                ):  # Warning: if it can be set to False
                    product_id = int(link.get_attribute("id"))
                    print("ID", product_id, product_id % 2)
                    link.click()
                    time.sleep(3)
                    if not product_id % 2:
                        # link = masthead.find_element_by_id(str(product_id))
                        link.click()
                        time.sleep(3)

                    enable = False

            except StopIteration:
                enable = False

        # Go to targeted product information page
        link_itr = iter(link_lst)
        enable = True
        while enable:

            try:
                link = next(link_itr)

                if not link.get_attribute(
                    "data-state"
                ):  # Warning: if it can be set to False

                    link.click()
                    # time.sleep(3)
                    WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(
                        lambda drv: drv.find_element_by_id("product_info")
                    )

                    self.assertEqual(
                        driver.current_url,
                        self.live_server_url
                        + reverse(
                            "product:product",
                            args=[product_id, "result", product_id, query],
                        ),
                    )

                    # Check state
                    product = driver.find_element_by_id(str(product_id))
                    data_state = product.get_attribute("data-state")
                    self.assertEqual(data_state, "true")

                    product.click()
                    time.sleep(3)
                    data_state = product.get_attribute("data-state")
                    self.assertEqual(data_state, "false")

                    enable = False

            except StopIteration:
                enable = False

        # Go back to Result page
        back_lnk = driver.find_element_by_id("result_back_link")
        back_lnk.click()

        product_section = WebDriverWait(driver, SEARCH_TIMEOUT_S).until(
            lambda drv: drv.find_element_by_id("product_section")
        )

        self.assertEqual(
            driver.current_url,
            self.live_server_url + reverse("product:result", args=[query]),
        )

        # --- Set favorite with odd code ---
        favorite_link_lst = product_section.find_elements_by_tag_name("a")
        product_id_lst = []
        for favorite in favorite_link_lst:

            if favorite.get_attribute("data-state") is not None:
                product_id = int(favorite.get_attribute("id"))
                product_id_lst.append(product_id)
                print("ID", product_id, product_id % 2)
                favorite.click()
                time.sleep(3)
                if not product_id % 2:
                    product_id_lst.pop()
                    favorite_link = product_section.find_element_by_id(str(product_id))
                    favorite_link.click()
                    time.sleep(3)

        # --- Go to Favorite page ---
        favorite_page_link = driver.find_element_by_id("favorite_a")
        # favorite_link = WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(
        #                                     EC.element_to_be_clickable((By.ID, 'favorite_a')))
        favorite_page_link.click()
        time.sleep(7)
        # WebDriverWait(driver, DEFAULT_TIMEOUT_S).until(lambda drv: drv.find_element_by_id('product_section'))

        self.assertEqual(
            driver.current_url, self.live_server_url + reverse("product:favorite")
        )

        # Check each favorite state
        for favorite_id in product_id_lst:
            favorite_link = driver.find_element_by_id(str(favorite_id))
            data_state = favorite_link.get_attribute("data-state")
            self.assertEqual(data_state, "false")

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
        cls.USER_PWD = "dummy_pwd"
        email = "user@dummy.com"
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
            "user_query": "prince",
        }
        response = self.client.get(reverse("product:result", kwargs=data))
        self.assertEqual(response.status_code, 200)

    def test_front_favorite(self):
        """
        Test that Favorite page return 200
        """
        response = self.client.get(reverse("product:favorite"))
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
