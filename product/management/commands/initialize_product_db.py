import requests
from operator import itemgetter


from django.core.management.base import BaseCommand, CommandError
from product.models import ZCategory, ZProduct

# DIR_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(DIR_BASE)
# sys.path.append(DIR_BASE)
# from zopynfacts import products
from zopynfacts import products as source



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
        parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        """Init db"""

        # Update category db        
        category_lst = self.init_category_db()
        category_lst = []

        # Update product db
        self.init_product_db(category_lst)


        for poll_id in options['poll_ids']:
            # try:
            #     poll = Poll.objects.get(pk=poll_id)
            # except Poll.DoesNotExist:
            #     raise CommandError('Poll "%s" does not exist' % poll_id)

            # poll.opened = False
            # poll.save()
            self.stdout.write(self.style.SUCCESS('Successfully read poll "%s"' % poll_id))

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
        new_category_lst = []
        for idx, category_dct in enumerate(category_source_lst[:self.N_CATEGORY_MAX]):
            category_id = category_dct['id']
            obj, is_created = ZCategory.objects.get_or_create(identifier=category_id)
            if is_created:
                new_category_lst.append(category_id)
                print(idx, 'New category added to DB:', category_id, '-', category_dct['name'])

        print(len(new_category_lst), 'new categories added to DB:')


        return category_source_lst


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
                print('Deleted product #', product_db.code, product_db.name)
                ZProduct.objects.filter(code=product_db.code).delete()


        # Product from category source

        ## Get category from db

        ## Get all products of category from source
        for idx, category_dct in enumerate(category_lst):

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

        print('AZERTY')

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
        
        # product_targeted.categories.clear()

        categories_hierarchy_lst = data_dct['categories_hierarchy']
        # nutrient_levels = data_dct['nutrient_levels']
        # image = data_dct['image']
        del data_dct['code']
        del data_dct['categories_hierarchy']
        del data_dct['nutrient_levels']
        del data_dct['image']

        ## Update product
        n = ZProduct.objects.filter(code=product_code).update(**data_dct)
        # print('N:', n)

        ## Update relative categories
        for idx, category_id in enumerate(categories_hierarchy_lst):

            category_db, created = ZCategory.objects.get_or_create(identifier=category_id)
            # print(category_db, created)
            product_targeted.categories.add(category_db, through_defaults={'hierarchy_index': idx})
    #         # category_db.products.add(product_targeted, through_defaults={'hierarchy_index': idx} )
    #         # relation = ZCategory_Product.objects.create(product=product_targeted, category=category_db, hierarchy_index=idx)
    #         # relation.save()


