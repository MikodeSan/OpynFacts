#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 12:50:20 2019

@author: doZan
"""

import sys
import os
import shutil
import operator

import requests

# add 'main' package

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dat' ))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dat\\im' ))
from database_json import ZDataBase_JSON as database
from database_mysql_connector import ZDataBase_MySQL as database_mysql

class ZFact():
    '''
    classdocs
    '''

    DB_PATH = 'data\funding_db.json'
    IMAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dat\\im')


    def __init__(self, observer=None):
        '''
        Constructor
        '''
        # Get database back
        self.__db = database()
        self.__db_sql = database_mysql()

        if 0:                                       # forcing db validation
            self.__db_sql.commit()

        # Init. database if necessary
        if not self.__db_sql.is_completed():                    # not self.__db.get_categories():
            category_dict = self.__download_categories()

            self.__db.init_categories(category_dict)
            self.__db_sql.add_category(category_dict)

            self.__init_database_product()

            self.__db.save_db()

    def categories(self):
        
        # categories_lst = self.__db.get_categories_from_relation()
        categories_lst = self.__db_sql.get_category_data(is_filled=True)
        # categories_lst.sort(key=operator.itemgetter('name'))

        return categories_lst

    def category_data(self, category_id_lst):
        return self.__db_sql.get_category_data(is_filled=False, category_id_lst=category_id_lst)          # __db.get_categories_data(category_id_lst)

    def products_from_categories(self, categories_lst):

        selected_product_lst = self.__db_sql.products(categories_lst)       # __db.products(categories_lst)

        selected_product_lst.sort(key=operator.itemgetter('brands', 'name', 'nutrition_grades', 'nova_group'))
        
        return selected_product_lst

    def products(self, product_code_lst):
        
        return self.__db_sql.product_data(product_code_lst)                 # __db.product_data(product_code_lst)

    def alternative_products(self, product_code, category_id):

        product_data_dct = self.__db_sql.product_data([product_code])              # __db.product_data([product_code])
        selected_product_data_dct = product_data_dct[product_code]
        # selected_product_data_dct[database.KEY_PRODUCT_CODE] = product_code
        print(selected_product_data_dct)

        selected_product_data_lst = self.__db_sql.products([category_id])       # __db.products([category_id])
        alternative_product_lst = []

        for product_data_dct in selected_product_data_lst:

            # selected_product_data_dct[database.KEY_PRODUCT_CODE] \
            if product_data_dct[database.KEY_PRODUCT_CODE] != product_code \
                and (product_data_dct['nutrition_grades'] < selected_product_data_dct['nutrition_grades'] \
                    or (product_data_dct['nutrition_grades'] == selected_product_data_dct['nutrition_grades'] \
                        and product_data_dct['nova_group'] < selected_product_data_dct['nova_group'])) :

                # print(product_data_dct)
                # selected_product_data_lst.remove(product_data_dct)
                alternative_product_lst.append(product_data_dct)
                # print(len(selected_product_data_lst))

        alternative_product_lst.sort(key=operator.itemgetter('nutrition_grades', 'nova_group', 'brands', 'name'))

        return alternative_product_lst

    def __download_categories(self):

        # - Get List of category ---
        path = "https://fr-fr.openfoodfacts.org/categories.json"
        # path = "https://fr-en.openfoodfacts.org/categories.json"
        # path = "https://world.openfoodfacts.org/categories.json"

        response = requests.get(path)
        if response.status_code != 200:
            exit(1)
        # print(response)

        return response.json()

    def __init_database_product(self, n_category_max=720, n_product_max=50):

        if n_category_max > 0:

            category_idx = 0
            categories_lst = self.__db_sql.get_category_data()          # self.__db.get_categories()

            # Get categories
            # n_category_max = len(categories_lst)/10     # to debug
            while category_idx < n_category_max:

                # Get category url
                category_id = categories_lst[category_idx]['id']           # categories_lst[category_idx]
                category_url = categories_lst[category_idx]['url']          # self.__db.get_category_url(category_id)

                print('\t> Process category #{}. {}'.format(category_idx, category_id))

                # Get category pages
                is_first_page = True
                page_idx = 0
                n_product = 0
                n_scan = 0
                n_product_total = 1


                while (n_scan < n_product_total) and (n_product < n_product_max):
                    
                    if is_first_page:
                        
                        response = requests.get(category_url)
                        if response.status_code == 200:
                            if response.url != category_url:
                                category_url = response.url
                                # print(category_url, response.url)
                                # exit(1)
                        else:
                            exit(1)

                    category_page_path = category_url + '/{}.json'.format(page_idx+1)
                    # print(category_page_path)

                    [products_lst, n_scanned, n_total] = self.__download_product_from_category(category_page_path,
                                                                                            is_first_page=is_first_page)
                    # print(products_lst)

                    if is_first_page:
                        n_product_total = n_total
                        # print(n_product_total)
                        is_first_page = False

                    n_product = n_product + len(products_lst)
                    n_scan = n_scan + n_scanned

                    # add product lst to db
                    # self.__db.add_product(category_id, products_lst)
                    self.__db_sql.add_product(category_id, products_lst)

                    page_idx = page_idx + 1

                category_idx = category_idx + 1

            self.__db_sql.commit()
            print('\t> Database is completed: {}'. format(self.__db_sql.is_completed()))

        else:

            for idx, category_id in enumerate(self.__db.get_categories()):
                category_url = self.__db.get_category_url(category_id) + '.json'
                # print(category_url)
                self.__download_product_from_category(category_url)

    def __download_product_from_category(self, category_page_path, is_first_page=True):

        response = requests.get(category_page_path)

        category_page_dict = response.json()

        # Get n total products
        n_product_total = 0
        if is_first_page:
            n_product_total = category_page_dict['count']

        # Get products from page
        page_products_lst = category_page_dict['products']

        products_lst = []
        for product_idx, product_dict in enumerate(page_products_lst):
            # Get product data
            product_data_dict = self.__product_data_from_source(product_dict)

            if product_data_dict:
                products_lst.append(product_data_dict)
                # print(product_idx+1, product_data_dict)

        return [products_lst, len(page_products_lst), n_product_total]

    def __product_data_from_source(self, product_dict):

        extracted_data_dict = {}

        # Get products basic data from dict --

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
            
            if 0:
                if image_url:
                    r = requests.get(image_url, stream=True)
                    if r.status_code == 200:
                        image_path = self.IMAGE_PATH + "/{}".format(extracted_data_dict['code']) + "." + image_url.split(".")[-1]
                        # print(image_path)
                        with open(image_path, 'wb') as out_file:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw, out_file)
                            extracted_data_dict['image'] = image_path
                    else:
                        exit(1)

                    del r
        
        else:
            extracted_data_dict = {}

        return extracted_data_dict


#    @staticmethod
    @classmethod
    def __db_path(cls):

        directory_path = os.path.dirname(__file__)
        # with this path, we go inside the folder `data` and get the file.
        path_to_file = os.path.join(directory_path, cls.DB_PATH)
        #        print('db path_to_file', path_to_file)

        return path_to_file



if __name__ == "__main__":

    import logging as log


    log.basicConfig(level=log.DEBUG)
    log.info('Enable log to level: DEBUG')

    # model
    model = ZFact()


#    log.info(model._db)
#    log.info(model.get_project_list())
#
#    project_id_cur = model.current_project_id
#    db_event_lst = model.__get_db_event_list(project_id_cur)
##    db_event_lst = model._db['projects_list'][project_id_cur]['event_list']
#
#    data_row = np.empty((1, len(model._data_frame_label)), dtype=np.object)
#    print(model._data_frame_label)
#    print(data_row)
