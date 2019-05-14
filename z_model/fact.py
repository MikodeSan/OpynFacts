#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 12:50:20 2019

@author: doZan
"""

import sys
import os

import requests

# add 'main' package

# sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), '/dat' ))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from dat.database_json import ZDataBase_JSON as database



class ZFact():
    '''
    classdocs
    '''

    DB_PATH = 'data/funding_db.json'


    def __init__(self, observer=None):
        '''
        Constructor
        '''

        self.__db = database()

        if not self.__db.get_categories():
            category_dict = self.__download_categories()

            self.__db.init_categories(category_dict)

            self.__init_database_product()

            self.__db.save_db()

            self.__db.get_categories_from_relation()

    def categories(self):
        
        return self.__db.get_categories_from_relation()


    def __download_categories(self):

        # --- Get List of category ---
        path = "https://fr-fr.openfoodfacts.org/categories.json"
        # path = "https://fr-en.openfoodfacts.org/categories.json"
        # path = "https://world.openfoodfacts.org/categories.json"

        response = requests.get(path)
        print(response)

        return response.json()


    def __init_database_product(self, n_category_max=70, n_product_max=70):

        if n_category_max > 0:

            category_idx = 0
            categories_lst = self.__db.get_categories()

            # Get categories
            while category_idx < n_category_max:

                # Get category url
                category_id = categories_lst[category_idx]
                category_url = self.__db.get_category_url(category_id)
                print(category_idx+1, category_id)


                # Get category pages

                is_first_page = True
                page_idx = 0
                n_product = 0
                n_scan = 0
                n_product_total = 1


                while (n_scan < n_product_total) and (n_product < n_product_max):

                    category_page_path = category_url + '/{}.json'.format(page_idx+1)

                    [products_lst, n_scanned, n_total] = self.__download_product_from_category(category_page_path,
                                                                                            is_first_page=is_first_page)
                    if is_first_page:
                        n_product_total = n_total
                        print(n_product_total)
                        is_first_page = False

                    n_product = n_product + len(products_lst)
                    n_scan = n_scan + n_scanned


                    # add product lst to db
                    self.__db.add_product(category_id, products_lst)


                    page_idx = page_idx + 1

                category_idx = category_idx + 1


        else:

            for idx, category_id in enumerate(self.__db.get_categories()):
                category_url = self.__db.get_category_url(category_id) + '.json'
                print(category_url)
                self.__download_product_from_category(category_url)


    def __download_product_from_category(self, category_page_path, is_first_page=True, n_product_max=50):

        response = requests.get(category_page_path)
        #                    print(response)

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
            product_data_dict = self.__product_data(product_dict)

            if product_data_dict:
                products_lst.append(product_data_dict)
                print(product_idx+1, product_data_dict)

        return [products_lst, len(page_products_lst), n_product_total]

    def __product_data(self, product_dict):

        extracted_data_dict = {}

        # -- Get products basic data from dict --

        # code
        extracted_data_dict['code'] = product_dict['code']

        # name
        name = ''
        lg_lst = ['fr', 'en', 'es', '']
        key_generic_base = 'generic_name'
        key_product_base = 'product_name'
        lg_idx = 0
        is_found = False
        while lg_idx < len(lg_lst) and not is_found:

            key_generic = key_generic_base + lg_lst[lg_idx]
            key_product = key_product_base + lg_lst[lg_idx]

            if key_generic in product_dict:
                if product_dict[key_generic] != '':
                    name = product_dict[key_generic]
                    is_found = True

                elif key_product in product_dict:
                    if product_dict[key_product] != '':
                        name = product_dict[key_product]
                        is_found = True

            lg_idx = lg_idx + 1

        if name != '':
            extracted_data_dict['name'] = name

        # brands
        if 'brands' in product_dict:
            extracted_data_dict['brands'] = product_dict['brands']

        if len(extracted_data_dict) < 3:
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
