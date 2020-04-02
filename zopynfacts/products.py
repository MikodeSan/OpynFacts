# -*- coding: utf-8 -*-
from . import utils
import requests

from operator import itemgetter


def nutrition(reference_product_dct, n_product_max):
    """
    Find alternative product from openfoodfact database
    """

    alternative_product_lst = []
    n_top_product = 0
    category_idx = 0
    n_category_max = len(reference_product_dct['categories_hierarchy'])

    grade_max = utils.NutritionGrade.E.value
    nova_max = utils.Nova.NOVA_4
    popularity_min = -1


    category_lst = reference_product_dct['categories_hierarchy']


    while (n_top_product < n_product_max) and (category_idx < n_category_max):

        # Get nutrition grades repartition from category
        category = category_lst[category_idx]
        print('Category', category)

        count, grade_lst = get_nutrition_grade_repartition(category)
        print(count, grade_lst)

        for grade in grade_lst:
            # Get product from nutrition grade group
            print('Grade', grade)
            if grade <= grade_max:

                flag = False
                if grade == 'a':
                    flag = True

                criteria_dct = {'categories': category, 'nutrition_grades': grade}
                product_page_dct = advanced_search(criteria_dct, page_size=1000, locale='fr')
                print('Count', product_page_dct['count'])

                for idx, product_src_dct in enumerate(product_page_dct['products']):

                    product_data_dct = extract_data(product_src_dct)

                    # Get product better than known alternatine one
                    is_unknown = True
                    if product_data_dct:

                        code = product_data_dct['code']

                        for alternative_product in alternative_product_lst:
                            if code == alternative_product['code']:
                                is_unknown = False
                    else:
                        is_unknown = False

                    if is_unknown:
                        if (product_data_dct['nutrition_grades'] < grade_max) \
                            or (product_data_dct['nutrition_grades'] == grade_max and product_data_dct['nova_group'] < nova_max) \
                                or (product_data_dct['nutrition_grades'] == grade_max and product_data_dct['nova_group'] == nova_max and product_data_dct['unique_scans_n'] < popularity_min): 
                            
                            alternative_product_lst.append(product_data_dct)

                            # Sort list of alternatve product prior by nutrition grade, nova score, popularity
                            alternative_product_lst.sort(key=itemgetter('unique_scans_n'), reverse=True)
                            alternative_product_lst.sort(key=itemgetter('nova_group'))
                            alternative_product_lst.sort(key=itemgetter('nutrition_grades'))

                            n_alternative_product = len(alternative_product_lst)

                            for altern in alternative_product_lst:
                                
                                print('Alternative list:', idx, altern['code'], '\t',
                                                                altern['name'], '\t',
                                                                altern['categories_hierarchy'][0], '\t',
                                                                altern['nutrition_grades'], '\t',
                                                                altern['nova_group'], '\t',
                                                                altern['unique_scans_n'] )

                            # Keep the maximal number of alternative wished
                            if n_alternative_product > n_product_max:

                                # Update number of grade: 'a'
                                if flag:
                                    n_top_product += 1

                                alternative_product_lst.pop()

                                # Update critera Min
                                print('Update values', grade_max, nova_max, popularity_min)
                                grade_max = alternative_product_lst[-1]['nutrition_grades']
                                nova_max = alternative_product_lst[-1]['nova_group']
                                popularity_min = alternative_product_lst[-1]['unique_scans_n']

        category_idx += 1

    return alternative_product_lst


def get_nutrition_grade_repartition(category):

    # search grade repartition from category
    grades_dct = drilldown_search('category', category, 'nutrition-grades', locale='fr')

    # Sort nutrition grades
    count = grades_dct['count']
    nutrition_grade_lst = sorted(grades_dct['tags'], key=itemgetter('id')) 

    grade_lst = [grade['id'] for grade in nutrition_grade_lst]

    return count, grade_lst


def extract_data(product_dict):
    """
    Extract main product data from openfoodfact
    """
    extracted_data_dict = {}

    # code
    extracted_data_dict['code'] = product_dict['code']

    # name
    name = ''
    lg_lst = ['_fr', '_en', '_es', '']
    key_product_base = 'product_name'
    key_generic_base = 'generic_name'
    lg_idx = 0
    is_found = False
    while lg_idx < len(lg_lst) and is_found == False:

        key_product = key_product_base + lg_lst[lg_idx]
        key_generic = key_generic_base + lg_lst[lg_idx]

        if key_product in product_dict:
            if product_dict[key_product] != '':
                print(product_dict[key_product])
                name = product_dict[key_product]
                is_found = True
        
        if is_found == False and key_generic in product_dict:
            if product_dict[key_generic] != '':
                print(product_dict[key_generic])
                name = product_dict[key_generic]
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
    extracted_data_dict['categories_hierarchy'] = extract_category_hierarchy(product_dict)

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

def extract_category_hierarchy(product_dict):
    """
    Extract category hierarchy list from openfoodfact
    """

    # category hierarchy
    category_lst = []
    idx = 0

    if 'compared_to_category' in product_dict:
        category_lst.append(product_dict['compared_to_category'])
        idx += 1
        print('compared_to_category', category_lst)

    if 'categories_hierarchy' in product_dict:
        for category in reversed(product_dict['categories_hierarchy']):
            if category not in category_lst:
                category_lst.append(category)
                # print('categories_hierarchy', category_lst)

    # if 'categories_tags' in product_dict:
    #     for category in reversed(product_dict['categories_tags']):
    #         if category not in category_lst:
    #             category_lst.insert(idx, category)
    #             idx += 1
    #             print('categories_tags', category_lst)
    #         else:
    #             idx = category_lst.index(category)
                
    return category_lst

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

    return utils.fetch(url, json_file=False, app_name='zopynfact', system='django', app_version='Version 1.0', website=None)

def advanced_search(criteria_dct, ingredient_dct={}, nutriment_dct={},
                    page=1, page_size=20,
                    sort_by='unique_scans', locale='world'):
    """
    Perform an advanced search using Open Food Facts search engine.
    """
    parameters = {
        'action': 'process',
        'page': page,
        'page_size': page_size,
        'sort_by': sort_by,
        'json': 'true' }

    print(criteria_dct)
    idx = 0
    for criteria, value in criteria_dct.items():
        parameters['tagtype_{}'.format(idx)] = criteria
        if value[0] != '-':
            parameters['tag_contains_{}'.format(idx)] = 'contains'
        else:
            parameters['tag_contains_{}'.format(idx)] = 'does_not_contain'
        parameters['tag_{}'.format(idx)] = value
        idx += 1 
        print(parameters)
    geography_code = locale + '-' + utils.API_LANGUAGE_CODE

    url = utils.build_url(geography=geography_code,
                          service='cgi',
                          resource_type='search.pl',
                          parameters=parameters)
    print(url)

    return utils.fetch(url, json_file=False, app_name='zopynfact', system='django', app_version='Version 1.0', website=None)

def drilldown_search(criteria, value, criteria_filter, filter_value=None, locale='world'):
    """
    Perform an drilldown search by getting secondary criteria for products from main criteria.
    """

    geography_code = locale + '-' + utils.API_LANGUAGE_CODE

    url = utils.build_url(geography=geography_code,
                          resource_type=[criteria, value, criteria_filter],
                          parameters=filter_value)
    print(url)
    return utils.fetch(url, json_file=True, app_name='zopynfact', system='django', app_version='Version 1.0', website=None)


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

