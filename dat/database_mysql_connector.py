#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 15:37:19 2019

@author: doZan
"""

import sys
import os
import logging as lg

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

    TABLES = {}
    TABLES['manifest'] = (
        "CREATE TABLE `manifest` ("
        "  `version` CHAR(5) NOT NULL DEFAULT '1.0',"
        "  `is_completed` CHAR(1) NOT NULL DEFAULT 'F',"
        "  PRIMARY KEY (`version`)"
        ") ENGINE=InnoDB")

    TABLES['category'] = (
        "CREATE TABLE `category` ("
        "  `id` VARCHAR(256) NOT NULL,"
        "  `label` VARCHAR(255),"
        "  `n_product` MEDIUMINT UNSIGNED NOT NULL DEFAULT 0,"
        "  `category_url` VARCHAR(1023),"
        "  `same_as` VARCHAR(255),"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB")

    TABLES['product'] = (
        "CREATE TABLE `product` ("
        "  `code` VARCHAR(255) NOT NULL,"
        "  `brand` VARCHAR(255),"
        "  `label` VARCHAR(512),"
        "  `store` TEXT,"
        "  `product_url` VARCHAR(512),"
        "  `same_as` VARCHAR(255),"
        "  `nova_group` TINYINT,"
        "  `nutrition_grade` CHAR(1),"
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
        #         "unique_scans_n": -1,
        ") ENGINE=InnoDB")

    TABLES['relation_category_product'] = (
        "CREATE TABLE `relation_category_product` ("
        "  `category_id` VARCHAR(256) NOT NULL,"
        "  `product_code` VARCHAR(255) NOT NULL,"
        "  `category_hierarchy_index` TINYINT UNSIGNED,"
        "  PRIMARY KEY (`category_id`, `product_code`)"
        ") ENGINE=InnoDB")


    def __init__(self, observer=None):

        self.__lg = lg
        self.__lg.basicConfig(level=lg.DEBUG)

        # Connect to Relational Database Management System
        db_conn = self.__connect()

        if db_conn:

            # Check database
            cursor = db_conn.cursor()

            if 0:   # TODO: TO DELETE (reset db)
                # drop database
                self.__drop_database(cursor)

            # Use database
            try:
                self.__lg.info("\t> Use database '{}'".format(self.DB_NAME))
                cursor.execute("USE {}".format(self.DB_NAME))
                self.__lg.info("\t  - Database {} used".format(self.DB_NAME))

            except mysql.connector.Error as err:

                self.__lg.warning("\t  - Database '{}' does not exists.".format(self.DB_NAME))
                if err.errno == errorcode.ER_BAD_DB_ERROR:
                    # if database does not exist, then create database
                    self.__create_database(db_conn)
                    db_conn.database = self.DB_NAME
                else:
                    self.__lg.error(err)
                    exit(1)

        #         # Get Matchs list
        #         path_to_file = self.__db_path()

        #         self.__data = bkp.open_db(path_to_file)
        #         if not self.__data:
        #             self.__data = self.__init_db()
        #             self.save_db(True)

            self.__close_connection(db_conn)
        
        else:
            print("db connection failed")

    def is_completed(self):
        
        version = ''
        is_completed = False

        db_conn = self.__connect(True)

        if db_conn:

            # try:
            cursor = db_conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM manifest")
            row = cursor.fetchone()

            version = row[0]
            self.__lg.info("\t  - Database version used: {}".format(version))
            if row[1] == 'T':
                is_completed = True

            # except mysql.connector.Error as err:
            #     self.__lg.error(err)
            #     exit(1)            
            self.__close_connection(db_conn)

        return is_completed

    def commit(self):

        is_completed = False

        db_conn = self.__connect(True)

        if db_conn:
                    
            cursor = db_conn.cursor(buffered=True)

            cursor.execute("UPDATE {} SET {} = 'T' WHERE version = {}".format('manifest', 'is_completed', '1.0'))
            db_conn.commit()
            self.__close_connection(db_conn)

        return is_completed

    def add_category(self, json=None, observer=None):

        db_conn = self.__connect(True)

        if db_conn:

            cursor = db_conn.cursor(buffered=True)

            remote_data_dict = json
            n_categories_detected = 0
            n_redundancy = 0

            
            for idx, tag_dict in enumerate(remote_data_dict['tags']):

                #        print('#', idx, '.\t\t:', tag_dict['id'])
                category_id = tag_dict['id']

                # check category id.
                is_valid = False
                category = category_id.split(':')

                if len(category) == 2:
                    is_valid = True
                else:
                    self.__lg.warning('\t  - Maybe category id. has an unknown format {}'.format(category))

                if is_valid:

                    language_code = category[0]
                    label = category[-1]

                    # Insert new category
                    try:
                        
                        cmd = "INSERT INTO category (id, label, n_product, category_url"
                        value = "VALUES (%(id)s, %(label)s, %(n_product)s, %(category_url)s"
                        # "VALUES (%s, %s, %s, %s, %s)")

                        data = {'id': category_id, 'label': tag_dict['name'], 'n_product':  tag_dict['products'], 'category_url':  tag_dict['url']}
                        # data_category = ('totot', 'azerty', 123, 'M', 'aedaef')
                        
                        if 'sameAs' in tag_dict:
                            
                            cmd = cmd + ", same_as"
                            value = value + ", %(same_as)s" 

                            data['same_as'] = tag_dict['sameAs'][0]
                            
                        cmd = cmd + ") "
                        value = value + ")"

                        # self.__lg.debug("\t> {}. Insert new category '{}'".format(n_categories_detected, category_id))
                        command = (cmd + value)           
                        cursor.execute(command, data)

                        n_categories_detected = n_categories_detected + 1

                    except mysql.connector.Error as err:
                        
                        if err.errno == errorcode.ER_DUP_ENTRY :
                            n_redundancy = n_redundancy + 1
                            self.__lg.warning("\t  - {}".format(err))
                        else:
                            self.__lg.error("\t  - {}".format(err))
                            exit(1)
                            # emp_no = cursor.lastrowid

            # Make sure data is committed to the database
            db_conn.commit()

            self.__lg.debug("N categories detected: {}/{} - N categories redundancy: {}".format(n_categories_detected, remote_data_dict['count'], n_redundancy))

            self.__close_connection(db_conn)

    def get_category_data(self, category_id_lst=None):

        db_conn = self.__connect(True)

        if db_conn:

            cursor = db_conn.cursor(buffered=True)

            query = ("SELECT id, label, n_product, category_url FROM category ")
            cursor.execute(query)
            row = cursor.fetchone()

            category_data_lst = []
            print('Total Row(s):', cursor.rowcount)

            while row is not None:
                category_data_lst.append(list(row))
                # self.__lg.debug("\t  - Category data: {}".format(category_data_lst[-1]))
                row = cursor.fetchone()

            self.__close_connection(db_conn)

        return category_data_lst

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

#     def get_category_url(self, category_id):

#         return self.__data[self.KEY_CATEGORY][category_id]['url']


    def add_product(self, category_id, products_lst):

        n_redundancy = 0

        db_conn = self.__connect(True)

        if db_conn:

            cursor = db_conn.cursor(buffered=True)


            existing_product_lst = []

            for product_idx, product_dict in enumerate(products_lst):

                try:
                    # Insert new product
                    sql_command = "INSERT INTO product (code, brand, label, store, product_url, nova_group, nutrition_grade, image_url) " \
                                    "VALUES (%(code)s, %(brand)s, %(label)s, %(store)s, %(product_url)s, %(nova_group)s, %(nutrition_grade)s, %(image_url)s)"
                    data = {'code': product_dict['code'], 'brand': product_dict['brands'], 'label': product_dict['name'],
                            'store': product_dict['stores'],
                            'product_url':  product_dict['url'],
                            'nova_group': product_dict['nova_group'], 'nutrition_grade': product_dict['nutrition_grades'], 'image_url': product_dict['image']}

                    self.__lg.debug("\t> {}. Insert new product: #{}-{}".format(product_idx, product_dict['code'], product_dict['name']))
                    cursor.execute(sql_command, data)

                    # Insert new category/product relation
                    cmd = "INSERT INTO relation_category_product (category_id, product_code"
                    value = "VALUES (%(category_id)s, %(product_code)s"
                    data = {'category_id': category_id, 'product_code': product_dict['code']}
                    self.__lg.debug("\t> Insert new relation: {}-#{}-{}".format(category_id, product_dict['code'], product_dict['name']))

                    if category_id in product_dict['categories_hierarchy']:
                        category_idx = product_dict['categories_hierarchy'].index(category_id)

                        cmd = cmd + ", category_hierarchy_index"
                        value = value + ", %(category_hierarchy_index)s"

                        data['category_hierarchy_index'] = category_idx
                    else:
                        self.__lg.warning("\t  - {} not in hierarchy {}".format(category_id, product_dict['categories_hierarchy']))

                    cmd = cmd + ") "
                    value = value + ")"
                    sql_command = cmd + value                    

                    cursor.execute(sql_command, data)

                except mysql.connector.Error as err:
                    
                    if err.errno == errorcode.ER_DUP_ENTRY :
                        # TODO: Update product data
                        existing_product_lst.append({'code': product_dict['code'], 'label':product_dict['name']})
                        n_redundancy = n_redundancy + 1
                        self.__lg.warning("\t  - {}; {}".format(err, existing_product_lst[-1]))
                    else:
                        self.__lg.error("\t  - {}".format(err))
                   
                        exit(1)

            # Make sure data is committed to the database
            db_conn.commit()

            # print('N existing product into db', len(existing_product_lst))      # n_redundancy

            self.__close_connection(db_conn)

        return existing_product_lst

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

    def __connect(self, use_database=False):
        """ Connect to MySQL database """
    
        db_config = self.__read_db_config()

        db_config = {
            'user': 'app',
            'password': 'No@pp23',
            'host': 'localhost',
            'raise_on_warnings': True
            }

        if use_database:
            db_config['database'] = 'openfacts'
    
        cnx = None

        try:
            cnx = mysql.connector.connect(**db_config)

            if cnx.is_connected():
                self.__lg.info('\t  - Connected to MySQL database')

        except mysql.connector.Error as err:
        
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.__lg.warning("\t  - Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.__lg.warning("\t  - Database does not exist")
            else:
                self.__lg.warning(err)

            exit(1)

        return cnx

    def __read_db_config(self, filename='config.ini', section='sql_db'):
        """ Read database configuration file and return a dictionary object
        :param filename: name of the configuration file
        :param section: section of database configuration
        :return: a dictionary of database parameters
        """
        # create parser and read ini configuration file
        parser = ConfigParser()
        # print(parser.read(filename))
    
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
        
    def __create_database(self, database_connection):

        is_success = True

        cursor = database_connection.cursor()

        self.__drop_database(cursor)

        try:
            self.__lg.debug("\t> Create database '{}'".format(self.DB_NAME))
            cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'UTF8MB4'".format(self.DB_NAME))
            self.__lg.debug("\t  - Database created successfully.")

            self.__lg.debug("\t> Use database '{}'".format(self.DB_NAME))
            cursor.execute("USE {}".format(self.DB_NAME))
            self.__lg.debug("\t  - Database '{}' used".format(self.DB_NAME))

        except mysql.connector.Error as err:
            is_success = False
            self.__lg.error("\t  - Failed creating database: {}".format(err))
            exit(1)

        if is_success:

            for table_name, table_description in self.TABLES.items():
                    
                try:
                    self.__lg.debug("\t> Create table '{}' ".format(table_name))
                    cursor.execute(table_description)

                except mysql.connector.Error as err:

                    is_success = False

                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        self.__lg.error("\t  - Table '{}' already exists".format(table_name))
                    else:
                        self.__lg.error("\t  - {} ".format(err))

            try:
                self.__lg.debug("\t> Set table '{}'".format('manifest'))
                cursor.execute("INSERT INTO {} VALUES ('1.0', 'F')".format('manifest'))
                database_connection.commit()
                self.__lg.debug("\t  - Version and status set into manifest table")

            except mysql.connector.Error as err:
                exit(1)                

    def __drop_database(self, cursor):

        try:
            self.__lg.debug('\t> Drop database')
            cursor.execute("DROP DATABASE IF EXISTS {}".format(self.DB_NAME))

        except mysql.connector.Error as err:
            # if err.errno == errorcode.ER_DB_DROP_EXISTS:
            #     self.__lg.warning('\t  - {}'.format(err))
            # else:
            self.__lg.warning('\t  - {}'.format(err))

    @staticmethod
    def __close_connection(connection):

        connection.cursor().close()
        connection.close()

if __name__ == '__main__':

    print(get_python_lib())

    db = ZDataBase_MySQL()
    db.add_category()
