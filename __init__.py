# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 23:46:29 2019

@author: Asus
"""


if __name__ == '__main__':

    import requests


    # --- Get List of category ---
    
    path = "https://fr-en.openfoodfacts.org/categories.json"
#    path = "https://world.openfoodfacts.org/categories.json"

    response = requests.get(path)
    print(response)
    category_dict = response.json()

    category_lst = []
    for idx, tag_dict in enumerate(category_dict['tags']):
#        print('#', idx, '.\t\t:', tag_dict['id'])
        category_lst.append(tag_dict['id'])
                
    print("Openfoodfacts World Categories:", category_lst)
    print("N World categories detected: {}".format(category_dict['count']))


    # --- Get List of product winthin a category ---

    path = "https://fr-en.openfoodfacts.org/category/pizza.json"
    response = requests.get(path)
    print(response)
    product_dict = response.json()

    n_product_total = product_dict['count']

    n_product_gotten = product_dict['skip']
    n_product_2_get = product_dict['page_size']
    page_id = product_dict['page']

    n_page_total = n_product_total // product_dict['page_size']
    if n_product_total % product_dict['page_size']:
        n_page_total = n_page_total + 1
        
    for idx in list(range(1, n_page_total+1)):
        path = "https://fr-en.openfoodfacts.org/category/pizzas/{}.json".format(idx)
        response = requests.get(path)
        print(idx, response)
        page_dict = response.json()
        
        for product_idx, product_dict in enumerate(page_dict['products']):
            if 'product_name' in product_dict:
                print(product_idx, product_dict['code'], product_dict['product_name'])
            elif 'generic_name' in product_dict:
                print(product_idx, product_dict['code'], product_dict['generic_name'])
            else:
                print(product_idx, product_dict['code'], 'No Name')
                
                    
        
#    print(product_dict['page_size'])
#    print(product_dict['count'])
#    print(product_dict['count'])
