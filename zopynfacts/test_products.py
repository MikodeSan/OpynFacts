from . import products as script
import requests


# def test_search(monkeypatch):

#     geocoding_reply_dct = {"products":["kinder bueno"], "count": 1}
#     result_dct = {'address': '74300 Cluses, France', 'location': {'lat': 46.06039, 'lng': 6.580582}}

#     class ResponseMocked:

#         def __init__(self, status_code, data):
#             self.status_code = status_code
#             self.data = data

#         def json(self):
#             return self.data

#     def mockreturn(url):
#         return ResponseMocked(200, geocoding_reply_dct)

#     monkeypatch.setattr(requests, 'get', mockreturn)

#     assert script.search('confiture bonne maman')['products'] == ["kinder bueno"]


# def advanced_search(monkeypatch):

#     criteria_dct, ingredient_dct={}, nutriment_dct={},
#                     page=1, page_size=20,
#                     sort_by='unique_scans', locale='world'):

#     key = "azertyuiop"
#     result = "https://maps.googleapis.com/maps/api/staticmap?center=14.6332414%2C-61.03804399999999&zoom=15&size=240x240&maptype=roadmap&markers=color%3Ablue%7Clabel%3AP%7C14.6332414%2C-61.03804399999999&key={}".format(key)

#     maps = script.ZGMaps(key)

#     assert maps.static_map_request_url(14.6332414, -61.03804399999999) == result

#     geocoding_reply_dct = {'results': [{'address_components': [{'long_name': 'Cluses', 'short_name': 'Cluses', 'types': ['locality', 'political']}, {'long_name': 'Haute-Savoie', 'short_name': 'Haute-Savoie', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'Auvergne-Rhône-Alpes', 'short_name': 'Auvergne-Rhône-Alpes', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'France', 'short_name': 'FR', 'types': ['country', 'political']}, {'long_name': '74300', 'short_name': '74300', 'types': ['postal_code']}], 'formatted_address': '74300 Cluses, France', 'geometry': {'bounds': {'northeast': {'lat': 46.08459, 'lng': 6.608080999999999}, 'southwest': {'lat': 46.040365, 'lng': 6.546846899999999}}, 'location': {'lat': 46.06039, 'lng': 6.580582}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 46.08459, 'lng': 6.608080999999999}, 'southwest': {'lat': 46.040365, 'lng': 6.546846899999999}}}, 'place_id': 'ChIJicNpE94GjEcRuiD-B6wY98Y', 'types': ['locality', 'political']}], 'status': 'OK'}
#     result_dct = {'address': '74300 Cluses, France', 'location': {'lat': 46.06039, 'lng': 6.580582}}

#     class ResponseMocked:

#         def __init__(self, status_code, data):
#             self.status_code = status_code
#             self.data = data

#         def json(self):
#             return self.data

#     def mockreturn(url):
#         return ResponseMocked(200, geocoding_reply_dct)

#     monkeypatch.setattr(requests, 'get', mockreturn)

#     maps = script.ZGMaps(0)
#     assert maps.geocoding_request('cluses') == result_dct


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

