#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 15:37:19 2019

@author: doZan
"""

class ZDataBase_JSON(object):
    '''
    classdocs
    '''

    DB_PATH = './'
    KEY_CATEGORY = 'category'
    KEY_PRODUCT = 'product'


    def __init__(self, observer=None):

        self.__data = self.__init_db()


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


    def get_categories(self):

        return list(self.__data[self.KEY_CATEGORY].keys())

    def get_category_url(self, category_id):

        return self.__data[self.KEY_CATEGORY][category_id]['url']

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
