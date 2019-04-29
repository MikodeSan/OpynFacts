#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 09:20:07 2019

@author: mtoussaint
"""

import requests


def main():

    # --- Get List of category ---

    path = "https://fr-en.openfoodfacts.org/categories.json"
#    path = "https://world.openfoodfacts.org/categories.json"

    response = requests.get(path)
    print(response)

    category_dict = response.json()
    print('N categories: {}'.format(category_dict['count']))


    category_lst = []
    for idx, tag_dict in enumerate(category_dict['tags']):
#        print('#', idx, '.\t\t:', tag_dict['id'])
        category_lst.append(tag_dict['id'])

    print("Openfoodfacts World Categories:", category_lst)

    print(len(category_lst))


if __name__ == "__main__":

    main()
