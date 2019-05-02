#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 15:37:19 2019

@author: doZan
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utilities import backup as bkp


class ZDataBase_JSON(object):
    '''
    classdocs
    '''

    DB_PATH = './'
    KEY_CATEGORY = 'category'
    KEY_PRODUCT = 'product'


    def __init__(self, observer=None):

        # Get Matchs list
        path_to_file = self.__db_path()

        self.__data = bkp.open_db(path_to_file)
        if not self.__data:
            self.__data = self.__init_db()
            self.save_db(True)




    def init_categories(self, json, observer=None):

        remote_data_dict = json
        categories_dict = self.__data[self.KEY_CATEGORY]
        n_categories_detected = 0
        n_redundancy = 0

        for idx, tag_dict in enumerate(remote_data_dict['tags']):

#        print('#', idx, '.\t\t:', tag_dict['id'])
            category_id = tag_dict.pop("id")

            # check category id.
            is_valid = False
            category = category_id.split(':')

            if len(category) == 2:
                is_valid = True
            else:
                print('/!\\ Warning /!\\ Maybe category id. has an unknown format', category)

            if is_valid:

                language_code = category[0]
                label = category[-1]

                if category_id not in categories_dict:
                    categories_dict[category_id] = tag_dict
                    n_categories_detected = n_categories_detected + 1
                else:
                    print('/!\\ Warning /!\\ id. key:{} already exist'.format(n_categories_detected, category_id))
                    n_redundancy = n_redundancy + 1


        print("N World categories detected: {}/{}".format(n_categories_detected, remote_data_dict['count']))
#        print("Openfoodfacts categories:", categories_dict.keys())
#        print("Openfoodfacts World Categories values:", categories_dict.values())
        print("N redundancy:", n_redundancy)
#        self.__save_db(True)


    def get_categories(self):

        return list(self.__data[self.KEY_CATEGORY].keys())

    def get_category_url(self, category_id):

        return self.__data[self.KEY_CATEGORY][category_id]['url']

    def add_product(self, products_lst):

        existing_product_lst = []

        for product_idx, product_dict in enumerate(products_lst):

            code = product_dict['code']

            db_products_dict = self.__data[self.KEY_PRODUCT]
            if code not in db_products_dict:
                db_products_dict[code] = product_dict
                print(db_products_dict[code])

            else:
                # TODO: Update product data
                existing_product_lst.append({'code': code, 'name':product_dict['name']})

        print('N existing product into db', len(existing_product_lst))

#        self.__save_db(True)

        return existing_product_lst


    def save_db(self, is_temp=True):

        if is_temp:

            bkp.modif_db(self.__db_path(), self.__data)
        else:
            pass

    @classmethod
    def __init_db(cls):

        db = {}

        # db version
        db['version'] = '1.00.00'

        # db categories
        categories_dict = {}
#        categories_dict['label'] = 'default'

        db[cls.KEY_CATEGORY] = categories_dict

        # db products
        products_dict = {}
#        categories_dict['label'] = 'default'

        db[cls.KEY_PRODUCT] = products_dict

#        print(db)

        return db

    @staticmethod
    def __db_path():

        directory_path = os.path.dirname(__file__)
        # with this path, we go inside the folder `data` and get the file.
        path_to_file = os.path.join(directory_path, "food_facts_db.json")
#        print('db path_to_file', path_to_file)

        return path_to_file


