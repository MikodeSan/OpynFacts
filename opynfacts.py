#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 09:20:07 2019

@author: doZan
"""

import sys
import os
import argparse
import logging as lg

import requests

# add 'model' package
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'z_model'))
from fact import ZFact as ZModel


# add 'view' package
# current working directory os.getcwd()

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'z_view'))
from opynfacts_view import ZOpynFacts_View as ZView

from PyQt5.QtWidgets import QApplication


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--extension", help="""Type of file to analyse. Is it a CVS or XML?""")
    parser.add_argument("-d", "--datafile", help="""the path of file to analyse""")
    parser.add_argument("-v", "--verbose", action='store_true', help="""Make the application talk!""")

    return parser.parse_args()

def main():

#        args = parse_arguments()
#
#    print('datafile path:', args.datafile)
#    print('args:', args)
#
#    if args.verbose:
#        lg.basicConfig(level=lg.DEBUG)
#    else:
#        lg.basicConfig(level=lg.DEBUG)
#        print('Enable log', lg.info)
#        lg.info('Enable log')
#
#    if args.extension == 'xml':
#        print('xml analysis')
#    elif args.extension == 'csv':
#        print('csv analysis')
#    else:
#        print('unknown file extension')
#
#    lg.info('Start Application')


        # model
    model = ZModel()


    APP = QApplication(sys.argv)

    UI = ZView(model)
    UI.show()

    sys.exit(APP.exec_())


#     # --- Get List of category ---

#     path = "https://fr-en.openfoodfacts.org/categories.json"
# #    path = "https://world.openfoodfacts.org/categories.json"

#     response = requests.get(path)
#     print(response)

#     category_dict = response.json()
#     print('N categories: {}'.format(category_dict['count']))


#     category_lst = []
#     for idx, tag_dict in enumerate(category_dict['tags']):
# #        print('#', idx, '.\t\t:', tag_dict['id'])
#         category_lst.append(tag_dict['id'])

#     print("Openfoodfacts World Categories:", category_lst)

#     print(len(category_lst))


if __name__ == "__main__":

    main()
