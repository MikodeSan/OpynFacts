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


    def __init__(self, observer=None):

        self.__data = self.__init_db()


    def init_categories(self, json, observer=None):

        remote_data_dict = json
        categories_dict = self.__data['categories']
        n_redundancy = 0

        for idx, tag_dict in enumerate(remote_data_dict['tags']):

#        print('#', idx, '.\t\t:', tag_dict['id'])
            category_id = tag_dict.pop("id")

            if category_id not in categories_dict:
                categories_dict[category_id] = tag_dict
            else:
                print('/!\\ Warning /!\\ id. key:{} already exist'.format(category_id))
                n_redundancy = n_redundancy + 1


        print("N World categories detected: {}".format(remote_data_dict['count']))
        print("Openfoodfacts World Categories:", categories_dict.keys())
        print("Openfoodfacts World Categories values:", categories_dict.values())
        print("N redundancy:", n_redundancy)


    def get_categories(self):

        return list(self.__data['categories'].keys())



    @classmethod
    def __init_db(cls):

        db = {}

        # db version
        db['version'] = '1.00.00'

        # db properties
        categories_dict = {}
#        categories_dict['label'] = 'default'
#        categories_dict['project_id_cur'] = 0
#        categories_dict['credit_id_next'] = 0
#        categories_dict['transaction_id_next'] = 0
#
        db['categories'] = categories_dict
#
#        # db projects list
#        db['projects_list'] = []
#
#        # project_0
#        project = {}
#        db['projects_list'].append(project)
#
#        project['event_list'] = []
#        project['enabled'] = True
#        project['label'] = 'Project_Demo_0'
#        project['capital'] = 20000
#        project['yearly_rate_percent'] = 1.5
#        project['period_mth'] = 60
#        project['monthly_payment'] = 700
#        project['credit_list'] = []
#
#        credit = {}
#        credit['credit_label'] = 'Credit_0'
#        credit['capital'] = 20000
#        credit['yearly_rate_percent'] = 4
#        credit['period_mth'] = 24
#        credit['monthly_payment'] = -1
#
#        project['credit_list'].append(credit)
#
#
#
#
#        db['projects_list'].append(project)

#        print(db)

        return db
