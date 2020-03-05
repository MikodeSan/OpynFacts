# -*- coding: utf-8 -*-
import utils
import requests


def search(query, page=1, page_size=20,
           sort_by='unique_scans', locale='world'):
    """
    Perform a search using Open Food Facts search engine.
    """
    # parameters = {'search_terms': query,
    #               'page': page,
    #               'page_size': page_size,
    #               'sort_by': sort_by,
    #               'json': '1'}

    # url = utils.build_url(geography=locale,
    #                       service='cgi',
    #                       resource_type='search.pl',
    #                       parameters=parameters)


    # # - Get List of category ---
    # path = "https://fr-fr.openfoodfacts.org/categories.json"
    # # path = "https://fr-en.openfoodfacts.org/categories.json"
    # # path = "https://world.openfoodfacts.org/categories.json"

    path = "https://fr.openfoodfacts.org/cgi/search.pl?action=process&search_terms={}&search_simple=1&page_size=1000&json=true".format(query)
    
    return utils.fetch(path, json_file=False)


def advanced_search(post_query):
    """
    Perform advanced search using OFF search engine
    """
    post_query['json'] = '1'
    url = utils.build_url(service='cgi',
                          resource_type='search.pl',
                          parameters=post_query)
    return utils.fetch(url, json_file=False)



if __name__ == "__main__":

    dct = search("nutella")
    product_lst = dct['products']
    for idx, product in enumerate(product_lst):

        scan = 0
        if 'unique_scans_n' in product:
            scan = product['unique_scans_n']
            
        print(idx, product['code'], scan)