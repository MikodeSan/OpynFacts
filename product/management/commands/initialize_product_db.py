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

        # Update category db        
        category_lst = self.init_category_db()

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

        # Init db

        # Init category db

        ## Get Categories from db

        ## Get new categories 
        category_source_lst = source.get_categories(self.LOCALE, self.LANGAGE)
        Ncat_src = len(category_source_lst)
        print('Raw Categories count:', Ncat_src)

        # nCategory_cur = Ncat_src
        category_idx = Ncat_src-1

        category_lst = []

        while category_idx >= 0:

            ### Get existing Categories from source
            is_stored = False

            if is_stored:
                category_dct = category_source_lst.pop(category_idx)
                print(category_idx, category_dct)
                category_lst.append(category_dct)

            else:
                ### Discard non-valid categories from source
                is_valid = False
                category_dct = category_source_lst[category_idx]

                # if 'known' in category_dct and 'sameAs' in category_dct:
                if 'known' in category_dct:
                    if category_dct['known'] == 1:
                        is_valid = True

                if not is_valid:
                    category_dct = category_source_lst.pop(category_idx)

                    # print(category_idx, 'Poped category:', category_dct, 'Source count', len(category_source_lst))

            category_idx -= 1

        print('Final Categories count:', len(category_source_lst))

        ## Add new categories
        Nmax = self.N_CATEGORY_MAX
        Ncategory = len(category_lst)
        if Ncategory < Nmax:
            ### Get most complete/full categories
            n = Nmax - Ncategory
            category_lst.extend(category_source_lst[:n])

        for idx, cat_dct in enumerate(category_lst):
            print(idx, 'Category:', cat_dct['name'], '-', cat_dct['products'], 'Products')

        ## Update categories into db (new and existing)


        return category_lst


    def init_product_db(self, category_lst):

        # Update existing product from db

        ## Get all product from db
        product_lst = []

        ## Get products from source
        for idx, product_dct in enumerate(product_lst):

            product_id = product_dct['id']
            ### download product
            product_dct = source.get_product(product_id, locale=self.LOCALE)
            print(product_dct['code'])

            ### extract data
            product_data_dct = source.extract_data(product_dct)
    
            ## Update db
            # set_product_model()




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
