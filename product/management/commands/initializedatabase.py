import os
import sys

import requests
from operator import itemgetter
import logging
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

APP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
B_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print(APP_DIR)
print(B_DIR)
sys.path.append(APP_DIR)
sys.path.append(B_DIR)

from product.models import ZCategory, ZProduct


# from zopynfacts import products
from zopynfacts import products as source


# Get an instance of a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)

logger.addHandler(ch)


class Command(BaseCommand):
    help = 'Initialize or alternately Update Product module database'

    LOCALE = 'fr'
    LANGAGE_DEFAULT = 'en'
    LANGAGE = 'fr'

    N_CATEGORY_MAX = 17         # 50
    N_PRODUCT_MAX = 23          # 50
    N_POPULAR_MAX = 17          # 23
    N_HEALTHY_MAX = 7           # 12


    def add_arguments(self, parser):
        parser.add_argument('zargs', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        """Init db"""

        print(logger, datetime.datetime.now())
        logger.info('Initialize biggest category list into db', exc_info=True, extra={
            # Optionally pass a request and we'll grab any information we can
            'request': '1',
            })
        # logger.warning('Initialize database')
        # logger.error('Initialize database', exc_info=True, extra={
        #     # Optionally pass a request and we'll grab any information we can
        #     'request': 'toto',
        #     })
        # logger.critical('Initialize database', exc_info=True, extra={
        #     # Optionally pass a request and we'll grab any information we can
        #     'request': 'toto',
        #     })

        # Initialize biggest category list into db
        print('> Initialize biggest category list into dbs', datetime.datetime.now())
        category_lst, category_source_lst = self.init_category_db()

        # # Update product db
        # print('> Update product into db')
        # self.init_product_db(category_lst)

        # # Update category fields
        # print('> Update category fields')
        # category_update_lst = []
        
        # # ## Method #1: scan each category from source list then check and update existing category from db
        # # for idx, category_src_dct in enumerate(category_source_lst):
            
        # #     try:
        # #         category_db = ZCategory.objects.get(identifier=category_src_dct['id'])
        # #     except ObjectDoesNotExist:
        # #         pass
        # #     except :
        # #         print('CRITICAL EXCEPTION: exit from category fields update')
        # #         exit(1)
        # #     else:
        # #         category_name = category_src_dct['name']
        # #         ZCategory.objects.filter(identifier=category_src_dct['id']).update(label=category_name)
        # #         category_update_lst.append(category_name)
        # #         print(len(category_update_lst), idx, 'Update category name', category_name)

        # ## Method #2: scan each category from db then check and update existing category from source
        # category_lst_db = ZCategory.objects.all()

        # for idx, category_db in enumerate(category_lst_db):
        #     category_db_id = category_db.identifier

        #     category_src_dct = next((category_dct for idx, category_dct in enumerate(category_source_lst) if category_dct["id"] == category_db_id), None)
        #     # category_lst = list(filter(lambda category_dct: category_dct['id'] == category_db_id, category_source_lst))
        #     if category_src_dct:
        #         category_name = category_src_dct['name']
        #         ZCategory.objects.filter(identifier=category_src_dct['id']).update(label=category_name)
        #         category_update_lst.append(category_name)
        #         print(len(category_update_lst), idx, 'Update category name', category_name)
        #     else:
        #         print('Category', category_db_id, 'not found in source')

        for arg in options['zargs']:
            self.stdout.write(self.style.SUCCESS('Successfully read arg "%s"' % arg))


    def init_category_db(self):
        """
        Initialize and update category db with the biggest/most complete ones from source
        """

        ## Get categories from source
        category_source_lst = source.get_categories(self.LOCALE, self.LANGAGE)
        n_cat = len(category_source_lst)
        print('Raw Categories count:', n_cat)

        # ## Discard non-valid categories from source
        # category_idx = n_cat-1

        # while category_idx >= 0:

        #     is_valid = False
        #     category_dct = category_source_lst[category_idx]

        #     # if 'known' in category_dct and 'sameAs' in category_dct:
        #     if 'known' in category_dct:
        #         if category_dct['known'] == 1:
        #             is_valid = True

        #     if not is_valid:
        #         category_dct = category_source_lst.pop(category_idx)
        #         # print(category_idx, 'Poped category:', category_dct, 'Source count', len(category_source_lst))

        #     category_idx -= 1
        # print('Final Categories count:', len(category_source_lst))

        ## Get Biggest categories
        ### sort by amount of products (useless because are already sorted from source)

        ## Add new categories into db
        category_lst = category_source_lst[:self.N_CATEGORY_MAX]
        new_category_lst = []

        for idx, category_dct in enumerate(category_lst):
            category_id = category_dct['id']
            obj, is_created = ZCategory.objects.get_or_create(identifier=category_id)
            if is_created:
                new_category_lst.append(category_id)
                print(idx, 'New category added to DB:', category_id, '-', category_dct['name'])

        print(len(new_category_lst), 'new categories added to DB')

        return category_lst, category_source_lst


    def init_product_db(self, category_lst):

        # Update existing product from db

        ## Get all product from db
        # for idx in range()
        # offset = 0
        # step = 10
        product_lst_db = ZProduct.objects.all()            # [offset:step]
        for product_db in product_lst_db:

            ## Get products from source
            # print(product_db.code)
            product_response_dct = source.get_product(str(product_db.code), locale=self.LOCALE)
            if 'product' in product_response_dct:
                product_dct = product_response_dct['product']
            
                ### extract data
                product_data_dct = source.extract_data(product_dct)

                ## Update db
                update_product_db(product_data_dct, force=True)

                # product_code_lst.append(str(product_db.code))
            else:
                print('/!\\Warning/!\\: Product #', product_db.code, product_db.name, 'Not in source any more')
                # ZProduct.objects.filter(code=product_db.code).delete()

        print('Existing products updated')


        # Add new product from category source into db

        new_product_lst = []
        for idx, category_dct in enumerate(category_lst):

            ## Get products of category from source
            category_id = category_dct['id']
            category_url = category_dct['url']

            product_lst = source.get_products_from_category(category_url, self.N_PRODUCT_MAX)
            print('\t> {}. Process category #{} - {} Products'.format(idx, category_id, len(product_lst)))
            # for idx, p in enumerate(product_lst):
            #     print(idx, p['code'], p['name'], p['unique_scans_n'])

            best_product_lst = []

            ### Get most popular product. Sort list of products prior by popularity
            product_lst.sort(key=itemgetter('unique_scans_n'), reverse=True)

            best_product_lst.extend(product_lst[:self.N_POPULAR_MAX]) 
            # for idx, p in enumerate(best_product_lst):
            #     print(idx, p['code'], p['name'], p['unique_scans_n'])
            
            ### Get healthiest product. Sort list of product prior by nutrition grade, nova score
            product_lst.sort(key=itemgetter('nova_group'))
            product_lst.sort(key=itemgetter('nutrition_grades'))

            for product_dct in product_lst[:self.N_HEALTHY_MAX]:
                #### Add only new product into final product list
                if not any(product_dct['code'] in dct.values() for dct in best_product_lst):
                    best_product_lst.append(product_dct) 
            
            for idx, p in enumerate(best_product_lst):
                print(idx, p['code'], p['name'], p['nutrition_grades'], p['nova_group'], p['unique_scans_n'])

            ## add only new products into db

            for idx, product_dct in enumerate(best_product_lst):

                ### Create new product
                product_code = product_dct['code']
                obj, is_created = ZProduct.objects.get_or_create(code=product_code)
                if is_created:

                    ### Update new product into db
                    new_product_lst.append(product_code)

                    update_product_db(product_dct, force=True)
                    print('New product added to DB:', idx,  '#', product_code, '-', product_dct['brands'], '-', product_dct['name'])

        print('Total', len(new_product_lst), 'new products added to DB')

        # Get existing cat from 
        
        # nCategory = 50
        # delta = Ncat_src // nCategory
        # print('DELTA', delta)

        # cat_lst = [el_dct for idx, el_dct in enumerate(categories_dct['tags']) if idx % delta == 0]
        # for idx, cat_dct in enumerate(cat_lst):
        #     print(idx, cat_dct)

def update_product_db(data_dct, force=False):
    """
    Update object from specified data
    """
    
    # print('DATA_DCT', data_dct)
    product_code = data_dct['code']

    product_targeted = ZProduct.objects.get(code=product_code)
    # print("Product get:", product_targeted)

    if force or (not force and product_targeted.last_modified_t < data_dct['last_modified_t']):

        ## Clean parameter
        categories_hierarchy_lst = data_dct['categories_hierarchy']
        del data_dct['code']
        del data_dct['categories_hierarchy']
        del data_dct['nutrient_levels']
        del data_dct['image']

        ## Update product
        n = ZProduct.objects.filter(code=product_code).update(**data_dct)
        # print('N:', n)

        ## Update relative categories
        product_targeted.categories.clear()

        for idx, category_id in enumerate(categories_hierarchy_lst):

            category_db, created = ZCategory.objects.get_or_create(identifier=category_id)
            # print(category_db, created)
            product_targeted.categories.add(category_db, through_defaults={'hierarchy_index': idx})
    #         # category_db.products.add(product_targeted, through_defaults={'hierarchy_index': idx} )
    #         # relation = ZCategory_Product.objects.create(product=product_targeted, category=category_db, hierarchy_index=idx)
    #         # relation.save()



if __name__ == '__main__':

    # APP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # PJ_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    # print(APP_DIR)
    # print(B_DIR)
    # sys.path.append(APP_DIR)
    # sys.path.append(B_DIR)

    # from product.models import ZCategory, ZProduct

    Command.handle(0)