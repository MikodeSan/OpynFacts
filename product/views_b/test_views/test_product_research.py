import os
import sys
import json
from _pytest.monkeypatch import MonkeyPatch

from django.conf import settings as project_settings

sys.path.append(project_settings.BASE_DIR)

from test_util import *
from product.views_b import research as script

from zopynfacts import products


# Tests of Front for authenticated product pages
class TestFrontProductAuthenticatedMisc(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.monkeypatch = MonkeyPatch()

    def tearDown(self):
        pass

    def test_research_product_online(self):
        """
        Test that Result page returns a 200
        """
        user_query = "prince"

        # get dict from json
        directory_path = os.path.dirname(os.path.abspath(__file__))
        filename = "product_search_prince_dct.json"
        path_to_file = os.path.join(directory_path, filename)

        with open(path_to_file, "r") as myfile:

            db = json.load(myfile)
            product_dct = db["products"][0]

        # Mockup product search
        def mockreturn(
            query, page=1, page_size=20, sort_by="unique_scans", locale="world"
        ):
            return db

        self.monkeypatch.setattr(products, "search", mockreturn)

        # Search product from source, extract product data, and set product into db
        product_mdl = script.import_product_from_source(user_query)

        # check model attributes
        self.assertEqual(product_mdl.code, int(product_dct["code"]))
        self.assertEqual(product_mdl.brands, product_dct["brands"])
        self.assertEqual(product_mdl.name, product_dct["product_name"])
        self.assertEqual(product_mdl.url, product_dct["url"])
        self.assertEqual(product_mdl.nutrition_grades, product_dct["nutriscore_grade"])
        self.assertEqual(product_mdl.nova_group, product_dct["nova_group"])
        self.assertEqual(product_mdl.unique_scans_n, product_dct["unique_scans_n"])
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
