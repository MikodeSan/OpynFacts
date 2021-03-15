import os
import sys
import json
from _pytest.monkeypatch import MonkeyPatch

from django.conf import settings as project_settings

sys.path.append(project_settings.BASE_DIR)

from test_util import *
# from product.views_b import research as script

from product.models import ZProduct, ZCategory, ZSearch, ZCategory_Product
from zopynfacts import products


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
        self.monkeypatch = MonkeyPatch()


    def tearDown(self):
        # self.client.logout()
        pass


    def test_research_product_online(self):
        """
        Test that Result page returns a 200
        """
        data = {
            'user_query': 'prince',
        }

        user_query = 'prince'
        expected_product_model = None
        product_mdl = None


        # get dict from json

        directory_path = os.path.dirname(os.path.abspath(__file__))
        filename = "product_search_prince_dct.json"

        path_to_file = os.path.join(directory_path, filename)

        print(path_to_file)

        try:
            with open(path_to_file, "r") as myfile:
                try:
                    db = json.load(myfile)
                    if db:

                        product_dct = db['products'][0]
                    if not db:  # is_empty(db):
                        raise Exception(
                            "Database is empty"
                        )  # DatabaseEmptyWarning('Database is empty')
                except:
                    print("\n# <Exception> ", "Unexpected error:", sys.exc_info(), "\n#")

        except FileNotFoundError as err:
            print("\n# <Exception> ", err, "\n")


        # Mockup product search, 

        # mocked return function to replace Path.home
        # always return '/abc'
        def mockreturn(query, page=1, page_size=20,
           sort_by='unique_scans', locale='world'):
            return db
        # Application of the monkeypatch to replace Path.home
        # with the behavior of mockreturn defined above.
        self.monkeypatch.setattr(products, "search", mockreturn)

        r_json = products.search(user_query, locale='fr')

        # Calling getssh() will use mockreturn in place of Path.home
        # for this test with the monkeypatch.

        # extract product data

        # set product into db

        # check model attributes

        code = product_dct['code']
        product_mdl = ZProduct.objects.get(code=code)
        self.assertEqual(product_mdl.code, code)
        self.assertEqual(product_mdl.brands, product_dct['code'])
        self.assertEqual(product_mdl.name, product_dct['code'])
        self.assertEqual(product_mdl.url, product_dct['code'])
        self.assertEqual(product_mdl.nutrition_grades, product_dct['code'])
        self.assertEqual(product_mdl.nova_group, product_dct['code'])
        self.assertEqual(product_mdl.unique_scans_n, product_dct['code'])
        # self.assertEqual(product_mdl.code, product_dct['code'])


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
