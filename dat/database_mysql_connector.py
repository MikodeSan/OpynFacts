#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 15:37:19 2019

@author: doZan
"""

import sys
import os
import mysql.connector

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# from utilities import backup as bkp


from distutils.sysconfig import get_python_lib
from mysql.connector import errorcode
from configparser import ConfigParser



class ZDataBase_MySQL(object):
    '''
    classdocs
    '''

    DB_NAME = 'openfacts'
#     KEY_CATEGORY = 'category'
#     KEY_PRODUCT = 'product'
#     KEY_RELATION_CATEGORY_2_PRODUCT = 'category2product'
#     KEY_CATEGORY_ID = 'category_id'
#     KEY_PRODUCT_CODE = 'product_code'


    def __init__(self, observer=None):

        # Connect to Relational Database Management System
        db_conn = self.connect()

        # Check database
        # if database not exists, create database

#         # Get Matchs list
#         path_to_file = self.__db_path()

#         self.__data = bkp.open_db(path_to_file)
#         if not self.__data:
#             self.__data = self.__init_db()
#             self.save_db(True)

#     def init_categories(self, json, observer=None):

#         remote_data_dict = json
#         categories_dict = self.__data[self.KEY_CATEGORY]
#         n_categories_detected = 0
#         n_redundancy = 0

#         for idx, tag_dict in enumerate(remote_data_dict['tags']):

#             #        print('#', idx, '.\t\t:', tag_dict['id'])
#             category_id = tag_dict.pop("id")

#             # check category id.
#             is_valid = False
#             category = category_id.split(':')

#             if len(category) == 2:
#                 is_valid = True
#             else:
#                 print('/!\\ Warning /!\\ Maybe category id. has an unknown format', category)

#             if is_valid:

#                 language_code = category[0]
#                 label = category[-1]

#                 if category_id not in categories_dict:
#                     categories_dict[category_id] = tag_dict
#                     n_categories_detected = n_categories_detected + 1
#                 else:
#                     print('/!\\ Warning /!\\ id. key:{} already exist'.format(n_categories_detected, category_id))
#                     n_redundancy = n_redundancy + 1


#         print("N World categories detected: {}/{}".format(n_categories_detected, remote_data_dict['count']))
# #        print("Openfoodfacts categories:", categories_dict.keys())
# #        print("Openfoodfacts World Categories values:", categories_dict.values())
#         print("N redundancy:", n_redundancy)
# #        self.__save_db(True)


#     def get_categories(self):

#         return list(self.__data[self.KEY_CATEGORY].keys())

#     def get_categories_from_relation(self):
#         """Get valid categories from the category/product relation table
#         Then return the category data"""

#         category_id_lst = []
#         categories_lst = []
#         db_category_dct = self.__data[self.KEY_CATEGORY]

#         for element_dct in self.__data[self.KEY_RELATION_CATEGORY_2_PRODUCT]:

#             category_id = element_dct[self.KEY_CATEGORY_ID]

#             if category_id not in category_id_lst:

#                 # store collected category id 
#                 category_id_lst.append(category_id)
                
#                 data_dct = dict(db_category_dct[category_id])
#                 data_dct['id'] = category_id
#                 del data_dct['url']
#                 if 'sameAs' in data_dct:
#                     del data_dct['sameAs']
#                 categories_lst.append(data_dct)

#         return categories_lst


#     def get_categories_data(self, category_id_lst):

#         categories_dct = {}
#         db_categories_dct = self.__data[self.KEY_CATEGORY]

#         if category_id_lst:

#             for category_id in category_id_lst:

#                 if category_id in db_categories_dct:
#                     categories_dct[category_id] = db_categories_dct[category_id]

#         else:
#             categories_dct = dict(db_categories_dct)

#         return categories_dct


#     def get_category_url(self, category_id):

#         return self.__data[self.KEY_CATEGORY][category_id]['url']


#     def add_product(self, category_id, products_lst):

#         existing_product_lst = []
#         relation_lst = self.__data[self.KEY_RELATION_CATEGORY_2_PRODUCT]

#         for product_idx, product_dict in enumerate(products_lst):

#             code = product_dict.pop('code')
 
#             relation = {self.KEY_CATEGORY_ID:category_id, self.KEY_PRODUCT_CODE:code}
#             if relation not in relation_lst:
#                 relation_lst.append(relation)

#             db_products_dict = self.__data[self.KEY_PRODUCT]
#             if code not in db_products_dict:
#                 db_products_dict[code] = product_dict
#                 # print(db_products_dict[code])

#             else:
#                 # TODO: Update product data
#                 existing_product_lst.append({'code': code, 'name':product_dict['name']})

#         print('N existing product into db', len(existing_product_lst))

# #        self.__save_db(True)

#         return existing_product_lst

#     def products(self, categories_lst):

#         products_lst = []
#         db_products_dct = {}

#         # Get list of product code
#         if not categories_lst:

#             db_products_dct = dict(self.__data[self.KEY_PRODUCT])

#             for product_code, product_data_dct in db_products_dct.items():

#                 products_dct = product_data_dct
#                 products_dct[self.KEY_PRODUCT_CODE] = product_code
#                 products_lst.append(products_dct)

#         else:
#             product_code_lst = []
#             for category_id in categories_lst:

#                 for relation_dct in self.__data[self.KEY_RELATION_CATEGORY_2_PRODUCT]:

#                     if category_id == relation_dct[self.KEY_CATEGORY_ID]:
#                         product_code = relation_dct[self.KEY_PRODUCT_CODE]

#                         if product_code not in product_code_lst:
#                             product_code_lst.append(product_code)
#                             products_dct = dict(self.__data[self.KEY_PRODUCT][product_code])
#                             products_dct[self.KEY_PRODUCT_CODE] = product_code
#                             products_lst.append(products_dct)
#                             # print('product code', product_code)

#         return products_lst

#     def product_data(self, product_code_lst):

#         products_dct = {}
#         db_products_dct = self.__data[self.KEY_PRODUCT]
        
#         for product_code in product_code_lst:

#             if product_code in db_products_dct:
#                 products_dct[product_code] = dict(db_products_dct[product_code])

#         return products_dct

#     def save_db(self, is_temp=True):

#         if is_temp:

#             bkp.modif_db(self.__db_path(), self.__data)
#         else:
#             pass

#     @classmethod
#     def __init_db(cls):

#         db = {}

#         # db version
#         db['version'] = '1.00.00'

#         # db categories
#         categories_dict = {}
# #        categories_dict['label'] = 'default'

#         db[cls.KEY_CATEGORY] = categories_dict

#         # db products
#         products_dict = {}
# #        categories_dict['label'] = 'default'

#         db[cls.KEY_PRODUCT] = products_dict

#         # db relation
#         relation_lst = []
#         db[cls.KEY_RELATION_CATEGORY_2_PRODUCT] = relation_lst

# #        print(db)

#         return db

#     @staticmethod
#     def __db_path():

#         directory_path = os.path.dirname(__file__)
#         # with this path, we go inside the folder `data` and get the file.
#         path_to_file = os.path.join(directory_path, "food_facts_db.json")
# #        print('db path_to_file', path_to_file)

#         return path_to_file

    TABLES = {}
    TABLES['category'] = (
        "CREATE TABLE `category` ("
        "  `id` VARCHAR(127) NOT NULL,"
        "  `label` VARCHAR(255),"
        "  `n_product` MEDIUMINT UNSIGNED NOT NULL DEFAULT 0,"
        "  `url_str` VARCHAR(255),"
        "  `same_as` VARCHAR(255),"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")

    TABLES['product'] = (
        "CREATE TABLE `product` ("
        "  `code` MEDIUMINT UNSIGNED NOT NULL,"
        "  `label` VARCHAR(255),"
        "  `brand` VARCHAR(255),"
        "  `product_url` VARCHAR(255),"
        "  `same_as` VARCHAR(255),"
        "  `nova_group` TINYINT UNSIGNED,"
        "  `nutrition_grades` CHAR(1),"
        "  `image_url` VARCHAR(255),"
        "  PRIMARY KEY (`code`)"
        # "categories_hierarchy": [
        #             "en:biscuits-and-cakes",
        #             "en:cakes",
        #             "fr:financiers",
        #             "fr:P\u00e2tisseries fondantes \u00e0 la poudre d'amande"
        #         ],
        #         "created_t": 1480541444,
        #         "last_modified_t": 1558712294,
        #         "name": "P\u00e2tisseries fondantes \u00e0 la poudre d'amande.",
        #         "nutrient_levels": {
        #             "fat": "high",
        #             "salt": "moderate",
        #             "saturated-fat": "high",
        #             "sugars": "high"
        #         },
        #         "nutrition_score": -1,
        #         "nutrition_score_beverage": 0,
        #         "stores": "Bordeaux,Brive,Limoges,Saint-Yrieix",
        #         "unique_scans_n": -1,
        ") ENGINE=InnoDB")

    TABLES['relation_category_product'] = (
        "CREATE TABLE `relation_category_product` ("
        "  `category_id` VARCHAR(127) NOT NULL,"
        "  `product_code` MEDIUMINT UNSIGNED NOT NULL,"
        "  PRIMARY KEY (`category_id`, `product_code`)"
        ") ENGINE=InnoDB")




    def connect(self):
        """ Connect to MySQL database """
    
        db_config = self.read_db_config()

        db_config = {
            'user': 'app',
            'password': 'My@pp23',
            'host': 'localhost',
            'database': 'openfacts',
            'raise_on_warnings': True
            }
    
        cnx = None

        try:
            cnx = mysql.connector.connect(**db_config)

            if cnx.is_connected():
                print('Connected to MySQL database')

            cursor = cnx.cursor()

            try:
                cursor.execute("USE {}".format(self.DB_NAME))
            except mysql.connector.Error as err:
                print("Database {} does not exists.".format(self.DB_NAME))
                if err.errno == errorcode.ER_BAD_DB_ERROR:
                    create_database(cursor)
                    print("Database {} created successfully.".format(self.DB_NAME))
                    cnx.database = self.DB_NAME
                else:
                    print(err)
                    exit(1)

            for table_name in self.TABLES:
                table_description = self.TABLES[table_name]
                try:
                    print("Creating table {}: ".format(table_name), end='')
                    cursor.execute(table_description)
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        print("already exists.")
                    else:
                        print(err.msg)
                else:
                    print("OK")

            cursor.close()
            cnx.close()


        except mysql.connector.Error as err:
        
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        return cnx

    def read_db_config(self, filename='config.ini', section='sql_db'):
        """ Read database configuration file and return a dictionary object
        :param filename: name of the configuration file
        :param section: section of database configuration
        :return: a dictionary of database parameters
        """
        # create parser and read ini configuration file
        parser = ConfigParser()
        print(parser.read(filename))
    
        # print(parser)
        # print(parser.sections())
        # print(parser['DEFAULT'])
        # print(parser['bitbucket.org']['User'])
        # print(parser['topsecret.server.com'])
        # print(parser['DEFAULT'])
        
        # get section, default to mysql
        db = {}
        if parser.has_section(section):
            items = parser.items(section)
            print(items)
            for item in items:
                db[item[0]] = item[1]
        # else:
        #     raise Exception('{0} not found in the {1} file'.format(section, filename))
    
        return db
        
    def create_database(self, cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)


if __name__ == '__main__':

    print(get_python_lib())

    db = ZDataBase_MySQL()
