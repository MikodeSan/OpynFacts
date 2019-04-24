# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 23:46:29 2019

@author: Asus
"""


if __name__ == '__main__':

    import requests

    path = "https://world.openfoodfacts.org/categories.json"

    response = requests.get(path)


    print(response)

    j = response.json()
    print(j['count'])



    path = "https://world.openfoodfacts.org/category/plain-yogurts/2.json"

    response = requests.get(path)


    print(response)

    j = response.json()
    print(j['count'])
