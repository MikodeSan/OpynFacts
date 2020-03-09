from . import products as script
import requests


def test_search(monkeypatch):

    geocoding_reply_dct = {"products":["kinder bueno"], "count": 1}
    result_dct = {'address': '74300 Cluses, France', 'location': {'lat': 46.06039, 'lng': 6.580582}}

    class ResponseMocked:

        def __init__(self, status_code, data):
            self.status_code = status_code
            self.data = data

        def json(self):
            return self.data

    def mockreturn(url):
        return ResponseMocked(200, geocoding_reply_dct)

    monkeypatch.setattr(requests, 'get', mockreturn)

    assert script.search('confiture bonne maman')['products'] == ["kinder bueno"]


# def test_search(self):
#     with requests_mock.mock() as mock:
#         mock.get(
#             'https://world.openfoodfacts.org/cgi/search.pl?' +
#             'search_terms=kinder bueno&json=1&page=' +
#             '1&page_size=20&sort_by=unique_scans',
#             text='{"products":["kinder bueno"], "count": 1}')
#         res = openfoodfacts.products.search('kinder bueno')
#         self.assertEqual(res["products"],  ["kinder bueno"])
#         mock.get(
#             'https://world.openfoodfacts.org/cgi/search.pl?' +
#             'search_terms=banania&json=1&page=' +
#             '2&page_size=10&sort_by=unique_scans',
#             text='{"products":["banania", "banania big"], "count": 2}')
#         res = openfoodfacts.products.search(
#             'banania', page=2, page_size=10)
#         self.assertEqual(res["products"],  ["banania", "banania big"])

# def test_advanced_search(self):
#     with requests_mock.mock() as mock:
#         mock.get(
#             'https://world.openfoodfacts.org/cgi/search.pl?' +
#             'search_terms=coke&tagtype_0=packaging&' +
#             'tag_contains_0=contains&tag_0=plastic&' +
#             'nutriment_0=energy&nutriment_compare_0=gt&' +
#             'nutriment_value_0=0&sort_by=unique_scans&' +
#             'page_size=20',
#             text= '{"products":["Diet Coke"], "count": 1}')
#         res = openfoodfacts.products.advanced_search({
#                 "search_terms":"coke",
#                 "tagtype_0":"packaging",
#                 "tag_contains_0":"contains",
#                 "tag_0":"plastic",
#                 "nutriment_0":"energy",
#                 "nutriment_compare_0":"gt",
#                 "nutriment_value_0":"0",
#                 "sort_by":"unique_scans",
#                 "page_size":"20"
#             })
#         self.assertEqual(res["products"],["Diet Coke"])

