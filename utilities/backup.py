# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 13:16:57 2018

@author: mtt
"""

import os
import sys
import logging as lg
import shutil


#os.getcwd()         #sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# add 'main' package
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'utilities'))
from utilities import json_data as db_format


def new_db(filename):

    """" ... """
    # before start the new_fil gui, close and save current data if opened

    db_format.load_db(filename)

    # create new file

    # return path


def open_db(db_path):

    is_db_loaded = False

    # get path
    temp_path = temp_db_path(db_path)

    # if data temp exists, get tmp file
    if os.path.isfile(temp_path):
        # backup old db: TODO
        # switch files
        shutil.copyfile(temp_path, db_path)
        print("Info: %s file found" % temp_path)
        is_db_loaded = True
        try:
            os.remove(temp_path)
        except OSError as e:  ## if failed, report it back to the user ##
            print("Error: %s - %s." % (e.filename, e.strerror))
    else:    # Show an error #
        print("Warning: %s temp. file not found" % temp_path)
        if os.path.isfile(db_path):
            print("Info: %s file found" % db_path)
            is_db_loaded = True
        else:
            print("Error: %s file not found" % db_path)

    if is_db_loaded:
        db = db_format.load_db(db_path)
    else:
        db = {}
        
    # get data from cur_file
    return db


def save_db(filename):
    # if n > N_bkp [3;5;7;12] : del last 'date_hour.dbkp' file
    # cur <= tmp
    #
    pass


def saveas_db(filename):

    # return path
    pass


def modif_db(db_path, database):

    #    lg.info('[backup] modify db')

#    print('[backup] modify db')

    new_file_path = temp_db_path(db_path)

    db_format.save_db(new_file_path, database)


def close_db(filename):
    pass


def temp_db_path(db_path):

    path = os.path.dirname(db_path)
    file = os.path.basename(db_path)
    filename = os.path.splitext(file)[0]
    ext = os.path.splitext(file)[1]

    temp_file_path = path + '/' + '~' + filename + ext
    return temp_file_path


if __name__ == "__main__":

#        import logging as lg
#
#    lg.basicConfig(level=lg.DEBUG)
#    lg.info('Enable log to level DEBUG')
#
#    model = ZFunding()
#
#    lg.info(model._db)
#    lg.info(model.get_project_list())


    new_db("conso_data.json")
    pass
