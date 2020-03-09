# -*- coding: utf-8 -*-
from . import utils
import requests


def search(query, page=1, page_size=20,
           sort_by='unique_scans', locale='world'):
    """
    Perform a search using Open Food Facts search engine.
    """
    parameters = {
        'search_terms': query,
        'action': 'process',
        'page': page,
        'page_size': page_size,
        'sort_by': sort_by,
        'json': 'true' }

    url = utils.build_url(geography=locale,
                          service='cgi',
                          resource_type='search.pl',
                          parameters=parameters)
    # print(url)

    return utils.fetch(url, json_file=False)


def extract_data(product_dict):
    """Extract main product data from openfoodfact"""

    extracted_data_dict = {}


    # code
    extracted_data_dict['code'] = product_dict['code']

    # name
    name = ''
    lg_lst = ['_fr', '_en', '_es', '']
    key_generic_base = 'generic_name'
    key_product_base = 'product_name'
    lg_idx = 0
    is_found = False
    while lg_idx < len(lg_lst) and is_found == False:

        key_generic = key_generic_base + lg_lst[lg_idx]
        key_product = key_product_base + lg_lst[lg_idx]

        if key_generic in product_dict:
            if product_dict[key_generic] != '':
                print(product_dict[key_generic])
                name = product_dict[key_generic]
                is_found = True
        
        if is_found == False and key_product in product_dict:
            if product_dict[key_product] != '':
                print(product_dict[key_product])
                name = product_dict[key_product]
                is_found = True

        lg_idx = lg_idx + 1

    if name:
        extracted_data_dict['name'] = name
    else:
        extracted_data_dict['name'] = ''

    # brands
    extracted_data_dict['brands'] = ""
    if 'brands' in product_dict:
        extracted_data_dict['brands'] = product_dict['brands']

    # url
    extracted_data_dict['url'] = ""
    if 'url' in product_dict:
        extracted_data_dict['url'] = product_dict['url']
    
    # stores
    if 'stores' in product_dict:
        extracted_data_dict['stores'] = product_dict['stores'] # .split(',')
    else:
        extracted_data_dict['stores'] = ""

    # category hierarchy
    if 'categories_hierarchy' in product_dict:
        extracted_data_dict['categories_hierarchy'] = product_dict['categories_hierarchy']
    else:
        extracted_data_dict['categories_hierarchy'] = []

    if 'categories_tags' in product_dict:
        extracted_data_dict['categories_tags'] = product_dict['categories_tags']
    else:
        extracted_data_dict['categories_tags'] = []

    # nova group
    extracted_data_dict['nova_group'] = 127
    if 'nova_group' in product_dict:
        extracted_data_dict['nova_group'] = int(product_dict['nova_group'])
            
    # nutrition grade
    extracted_data_dict['nutrition_grades'] = 'z'
    if 'nutrition_grades' in product_dict:
        extracted_data_dict['nutrition_grades'] = product_dict['nutrition_grades']

    # nutrition score
    extracted_data_dict['nutrition_score'] = -1
    if 'nutriments' in product_dict:
        nutriments_dct = product_dict['nutriments']
        if 'nutrition-score-uk_100g' in nutriments_dct:
            score = nutriments_dct['nutrition-score-uk_100g']
        elif 'nutrition-score-fr_100g' in nutriments_dct:
            score = nutriments_dct['nutrition-score-fr_100g']
        elif 'nutrition-score-uk' in nutriments_dct:
            score = nutriments_dct['nutrition-score-uk']
        elif 'nutrition-score-fr' in nutriments_dct:
            score = nutriments_dct['nutrition-score-fr']

    # nutrient level
    extracted_data_dict['nutrient_levels'] = {}
    if 'nutrient_levels' in product_dict:
        extracted_data_dict['nutrient_levels'] = product_dict['nutrient_levels']

    # nutrition score beverage
    extracted_data_dict['nutrition_score_beverage'] = -1
    if 'nutrition_score_beverage' in product_dict:
        extracted_data_dict['nutrition_score_beverage'] = product_dict['nutrition_score_beverage']

    # unique_scans_n
    extracted_data_dict['unique_scans_n'] = -1
    if 'unique_scans_n' in product_dict:
        extracted_data_dict['unique_scans_n'] = product_dict['unique_scans_n']

    # nutrition score beverage
    extracted_data_dict['nutrition_score_beverage'] = -1
    if 'nutrition_score_beverage' in product_dict:
        extracted_data_dict['nutrition_score_beverage'] = product_dict['nutrition_score_beverage']
    
    # created time
    extracted_data_dict['created_t'] = -1
    if 'created_t' in product_dict:
        extracted_data_dict['created_t'] = product_dict['created_t']
    
    # last modified time
    extracted_data_dict['last_modified_t'] = -1
    if 'last_modified_t' in product_dict:
        extracted_data_dict['last_modified_t'] = product_dict['last_modified_t']

    extracted_data_dict['image'] = ""

    # if product data are valid
    if extracted_data_dict['name']:         # (extracted_data_dict['code'] < (2**64) and )

        # image
        image_url = ""
        if 'image_url' in product_dict:
            image_url = product_dict['image_url']
        elif 'image_front_url' in product_dict:
            image_url = product_dict['image_front_url']
        
        # if 0:
        #     if image_url:
        #         r = requests.get(image_url, stream=True)
        #         if r.status_code == 200:
        #             image_path = self.IMAGE_PATH + "/{}".format(extracted_data_dict['code']) + "." + image_url.split(".")[-1]
        #             # print(image_path)
        #             with open(image_path, 'wb') as out_file:
        #                 r.raw.decode_content = True
        #                 shutil.copyfileobj(r.raw, out_file)
        #                 extracted_data_dict['image'] = image_path
        #         else:
        #             exit(1)

        #         del r
    
        if image_url:
            extracted_data_dict['image_url'] = image_url
            
    else:
        extracted_data_dict = {}

    return extracted_data_dict


# # -*- coding: utf-8 -*-
# from . import utils
# import requests


# def get_product(barcode, locale='world'):
#     """
#     Return information of a given product.
#     """
#     url = utils.build_url(geography=locale,
#                           service='api',
#                           resource_type='product',
#                           parameters=barcode)
#     return utils.fetch(url)


# def get_by_facets(query, page=1, locale='world'):
#     """
#     Return products for a set of facets.
#     """
#     path = []
#     keys = query.keys()

#     if len(keys) == 0:
#         return []

#     else:
#         keys = sorted(keys)
#         for key in keys:
#             path.append(key)
#             path.append(query[key])

#         url = utils.build_url(geography=locale,
#                               resource_type=path,
#                               parameters=str(page))
#         return utils.fetch(url)['products']


# def add_new_product(post_data, locale='world'):
#     """
#     Add a new product to OFF database.
#     """
#     if not post_data['code'] or not post_data['product_name']:
#         raise ValueError('code or product_name not found!')

#     url = utils.build_url(geography='world',
#                           service='cgi',
#                           resource_type='product_jqm2.pl')
#     return requests.post(url, data=post_data)


# def upload_image(code, imagefield, img_path):
#     """
#     Add new image for a product
#     """
#     if imagefield not in ["front", "ingredients", "nutrition"]:
#         raise ValueError("Imagefield not valid!")

#     image_payload = {"imgupload_%s" % imagefield: open(img_path, 'rb')}

#     url = utils.build_url(service='cgi',
#                           resource_type='product_image_upload.pl')

#     other_payload = {'code': code, 'imagefield': imagefield}

#     headers = {'Content-Type': 'multipart/form-data'}

#     return requests.post(url=url,
#                          data=other_payload,
#                          files=image_payload,
#                          headers=headers)


# def advanced_search(post_query):
#     """
#     Perform advanced search using OFF search engine
#     """
#     post_query['json'] = '1'
#     url = utils.build_url(service='cgi',
#                           resource_type='search.pl',
#                           parameters=post_query)
#     return utils.fetch(url, json_file=False)
