#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 15:37:19 2019

@author: doZan
"""

import sys
import os
import logging as lg

import operator

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
    KEY_PRODUCT_CODE = 'product_code'

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
        "  `is_favorite` CHAR(1) NOT NULL DEFAULT 'F',"
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
        "  `category_hierarchy_index` TINYINT UNSIGNED DEFAULT 0,"
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

        db_conn = self.__connect(True)

        if db_conn:
                    
            cursor = db_conn.cursor(buffered=True)

            cursor.execute("UPDATE {} SET {} = 'T' WHERE version = {}".format('manifest', 'is_completed', '1.0'))
            db_conn.commit()
            self.__close_connection(db_conn)


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

    def get_category_data(self, is_filled=False, category_id_lst=None):

        category_data_lst = []

        db_conn = self.__connect(True)

        if db_conn:

            cursor = db_conn.cursor(buffered=True)

            if is_filled:
                # Get distinct filled categories from the category/product relation table

                category_id_lst = []

                query = ("SELECT DISTINCT category_id FROM relation_category_product")
                cursor.execute(query)
                row = cursor.fetchone()

                self.__lg.debug("\t  - Total categories selected from category/product relation table: {}".format(cursor.rowcount))

                while row is not None:

                    category_id = row[0]                  
                    # store collected category id 
                    category_id_lst.append(category_id)
                    # self.__lg.debug("\t  - Category id: {}".format(category_id_lst[-1]))
                        
                    row = cursor.fetchone()

            if category_id_lst:
                # Get specified category data from category table
            
                cursor.execute("SELECT COUNT(*) FROM category")
                (n_row, ) = cursor.fetchone()

                if len(category_id_lst) > 1:
                    query = ("SELECT * FROM category WHERE id IN {} ORDER BY label ASC".format( tuple(category_id_lst) ) )
                elif len(category_id_lst) == 1:
                    query = ("SELECT * FROM category WHERE id = '{}'".format( category_id_lst[0] ) )

                cursor.execute(query)
                self.__lg.debug("\t  - Total categories selected from id. list: {}/{} ({:.1%})".format(cursor.rowcount, n_row, cursor.rowcount/n_row ))

                row = cursor.fetchone()

            else:
                # Get specified category data from category table
                    
                query = ("SELECT * FROM category ORDER BY label ASC")
                cursor.execute(query)
                row = cursor.fetchone()

                self.__lg.debug("\t  - Total categories: {}".format(cursor.rowcount))

            while row is not None:

                category_dct = {}
                category_dct['id'] = row[0]
                category_dct['name'] = row[1]
                category_dct['products'] = row[2]
                category_dct['url'] = row[3]
                
                category_data_lst.append(category_dct)
                # self.__lg.debug("\t  - Category data: {}".format(category_data_lst[-1]))
                row = cursor.fetchone()

            self.__close_connection(db_conn)

        return category_data_lst


    def add_product(self, category_id, products_lst):

        n_redundancy = 0

        db_conn = self.__connect(True)

        if db_conn:

            cursor = db_conn.cursor(buffered=True)


            existing_product_lst = []

            for product_idx, product_dict in enumerate(products_lst):

                try:
                    # Insert new category/product relation
                    cmd = "INSERT INTO relation_category_product (category_id, product_code"
                    value = "VALUES (%(category_id)s, %(product_code)s"
                    data = {'category_id': category_id, 'product_code': product_dict['code']}
                    category_idx = -1

                    if category_id in product_dict['categories_hierarchy']:
                        category_idx = product_dict['categories_hierarchy'].index(category_id)
                    elif category_id in product_dict['categories_tags']:
                        category_idx = product_dict['categories_tags'].index(category_id)                        

                    if category_idx > -1:
                        cmd = cmd + ", category_hierarchy_index"
                        value = value + ", %(category_hierarchy_index)s"

                        data['category_hierarchy_index'] = category_idx
                    else:
                        self.__lg.warning("\t  - {} not in hierarchy {}_{}".format(category_id, product_dict['categories_hierarchy'], product_dict['categories_tags']))

                    cmd = cmd + ") "
                    value = value + ")"
                    sql_command = cmd + value                    

                    cursor.execute(sql_command, data)
                    self.__lg.debug("\t> Insert new relation: {}-#{}-{}-{}".format(category_id, product_dict['code'], product_dict['name'], category_idx))

                    # Insert new product
                    sql_command = "INSERT INTO product (code, brand, label, store, product_url, nova_group, nutrition_grade, image_url) " \
                                    "VALUES (%(code)s, %(brand)s, %(label)s, %(store)s, %(product_url)s, %(nova_group)s, %(nutrition_grade)s, %(image_url)s)"
                    data = {'code': product_dict['code'], 'brand': product_dict['brands'], 'label': product_dict['name'],
                            'store': product_dict['stores'],
                            'product_url':  product_dict['url'],
                            'nova_group': product_dict['nova_group'], 'nutrition_grade': product_dict['nutrition_grades'], 'image_url': product_dict['image']}

                    self.__lg.debug("\t> {}. Insert new product: #{}-{}".format(product_idx, product_dict['code'], product_dict['name']))
                    cursor.execute(sql_command, data)

                except mysql.connector.Error as err:
                    
                    if err.errno == errorcode.ER_DUP_ENTRY :
                        # TODO: Update product data
                        existing_product_lst.append({'code': product_dict['code'], 'label':product_dict['name']})
                        n_redundancy = n_redundancy + 1
                        self.__lg.warning("\t  - {}; {}; {}".format(err, category_id, existing_product_lst[-1]))
                    else:
                        self.__lg.error("\t  - {}".format(err))
                   
                        exit(1)

            # Make sure data is committed to the database
            db_conn.commit()

            # print('N existing product into db', len(existing_product_lst))      # n_redundancy

            self.__close_connection(db_conn)

        return

    def products(self, category_id_lst, is_favorite=False):

        product_lst = []

        db_conn = self.__connect(True)

        if db_conn:

            cursor = db_conn.cursor(buffered=True)

            try:
                if category_id_lst:

                    # Get product codes from filled categories
                    if len(category_id_lst) > 1:
                        query = ("SELECT DISTINCT product_code FROM relation_category_product WHERE category_id IN {}".format(tuple(category_id_lst)))
                    else:
                        query = ("SELECT DISTINCT product_code FROM relation_category_product WHERE category_id = '{}'".format(category_id_lst[0]))
                    cursor.execute(query)
                    self.__lg.debug("\t  - {} products selected from specified categories: {}".format(cursor.rowcount, category_id_lst))

                    row = cursor.fetchone()
                    product_id_lst = []

                    while row is not None:

                        # self.__lg.debug("\t  - Product code: {}".format(row))
                        product_id_lst.append(row[0])
                        row = cursor.fetchone()

                    # Get product data from product table
                    if len(product_id_lst) > 1:
                        query = ("SELECT * FROM product WHERE code IN {}".format( tuple(product_id_lst) ) )
                        cursor.execute(query)
                    elif len(product_id_lst) == 1:
                        query = ("SELECT * FROM product WHERE code = {}".format(product_id_lst[0]))
                        cursor.execute(query)

                    # self.__lg.debug("\t  - Total products selected from filled categories: {}".format(cursor.rowcount))

                    row = cursor.fetchone()

                else:
                    query = "SELECT * FROM product"

                    if is_favorite:
                        query = query + " WHERE is_favorite = 'T'"

                    cursor.execute(query)
                    self.__lg.debug("\t  - Total products selected from specified categories: {}".format(cursor.rowcount))

                    row = cursor.fetchone()

            except mysql.connector.Error as err:

                exit(1)


            while row is not None:
                products_dct = {}
                idx = 0

                products_dct[self.KEY_PRODUCT_CODE] = row[idx]
                idx = idx + 1
                products_dct['brands'] = row[idx]
                idx = idx + 1
                products_dct['name'] = row[idx]
                idx = idx + 1
                products_dct['stores'] = row[idx]
                idx = idx + 1
                products_dct['product_url'] = row[idx]
                idx = idx + 1
                products_dct['same_as'] = row[idx]
                idx = idx + 1
                products_dct['nova_group'] = row[idx]
                idx = idx + 1
                products_dct['nutrition_grades'] = row[idx]
                idx = idx + 1
                products_dct['image_url'] = row[idx]
                idx = idx + 1
                products_dct['is_favorite'] = True if row[idx] == 'T' else False                

                product_lst.append(products_dct)
                
                row = cursor.fetchone()

            self.__close_connection(db_conn)

        
        return product_lst

    def product_data(self, product_code_lst):

        product_dct = {}

        db_conn = self.__connect(True)

        if db_conn:

            cursor = db_conn.cursor(buffered=True)

            # Get product data from product table
            if product_code_lst:

                if len(product_code_lst) > 1:
                    query = ("SELECT * FROM product WHERE code IN {}".format( tuple(product_code_lst) ) )
                elif len(product_code_lst) == 1:
                    query = ("SELECT * FROM product WHERE code = {}".format(product_code_lst[0]))

                cursor.execute(query)
                self.__lg.debug("\t  - Total products selected from table: {}".format(cursor.rowcount))

                row = cursor.fetchone()

                while row is not None:

                    idx = 0

                    data_dct = {}
                    product_dct[row[0]] = data_dct

                    idx = idx + 1
                    data_dct['brands'] = row[idx]
                    idx = idx + 1
                    data_dct['name'] = row[idx]
                    idx = idx + 1
                    data_dct['stores'] = row[idx]
                    idx = idx + 1
                    data_dct['product_url'] = row[idx]
                    idx = idx + 1
                    data_dct['same_as'] = row[idx]
                    idx = idx + 1
                    data_dct['nova_group'] = row[idx]
                    idx = idx + 1
                    data_dct['nutrition_grades'] = row[idx]
                    idx = idx + 1
                    data_dct['image_url'] = row[idx]
                    
                    row = cursor.fetchone()

                # print(product_dct)

                # Get back filled category hierarchy of the product
                for product_code, product_data_dct in product_dct.items():

                    print(product_code, product_data_dct)
                    query = ("SELECT category_id, category_hierarchy_index FROM relation_category_product WHERE product_code = '{}'".format(product_code))

                    cursor.execute(query)
                    self.__lg.debug("\t  - Total category(ies) selected from product: {}".format(cursor.rowcount))

                    row = cursor.fetchone()

                    category_hierarchy_lst = [] 
                    while row is not None:

                        category_hierarchy_lst.append((row[0], row[1]))
                        row = cursor.fetchone()

                    print(category_hierarchy_lst)
                    
                    if category_hierarchy_lst:
                        category_hierarchy_lst.sort(key = operator.itemgetter(1), reverse=True)

                    for x in category_hierarchy_lst:
                        print(x[0])

                    product_data_dct['categories_hierarchy'] = [x[0] for x in category_hierarchy_lst]

            self.__close_connection(db_conn)

        return product_dct

    def set_favorite(self, product_code, is_added):

        db_conn = self.__connect(True)

        if db_conn:
                    
            try:
                cursor = db_conn.cursor(buffered=True)

                if is_added:
                    self.__lg.debug("\t  > Add #{} to favorite".format(product_code))
                    c = 'T'
                else:
                    self.__lg.debug("\t  > Remove #{} from favorite".format(product_code))
                    c = 'F'

                cursor.execute("UPDATE {} SET {} = '{}' WHERE code = {}".format('product', 'is_favorite', c, product_code))
                self.__lg.debug("\t  - Product #{} set to favorite".format(product_code))

            except mysql.connector.Error as err:
                self.__lg.error("\t  - Failed to add favorite")
                exit(1)

            db_conn.commit()
            self.__close_connection(db_conn)


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

            if not cnx.is_connected():
                self.__lg.info('\t  - Not Connected to MySQL database')

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
