#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 12:50:20 2019

@author: mtt
"""

import sys
import os

import requests

# add 'main' package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.append( os.path.join(os.path.dirname(__file__), '/dat' ))

from utilities import backup as bkp
from dat.database_json import ZDataBase_JSON as database



class ZFact(object):
    '''
    classdocs
    '''

    DB_PATH = 'data/funding_db.json'


    def __init__(self, observer=None):
        '''
        Constructor
        '''

        # Get Matchs list
#        path_to_file = ZFact.__db_path()
#
#        self._db = bkp.open_db(path_to_file)
#
#        self._db = {}

        db = database()

#        if not self._db:

        category_dict = self.__download_categories()

        db.init_categories(category_dict)


#            self._db = self.__init_db()
#            self.__save_db(True)

#        self._data_frame_label = self.__DATA_FRAME_LABEL
#
#        self.__cur_project_id = self._db['properties']['project_id_cur']

        print('\n All stored categories:\n', db.get_categories())

    def __download_categories(self):

        # --- Get List of category ---
        path = "https://fr-en.openfoodfacts.org/categories.json"
        #    path = "https://world.openfoodfacts.org/categories.json"

        response = requests.get(path)
        print(response)
#        print(response.json())

        return response.json()


    def __save_db(self, is_temp):

        if is_temp:

            bkp.modif_db(ZFact.__db_path(), self._db)
        else:
            pass


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
