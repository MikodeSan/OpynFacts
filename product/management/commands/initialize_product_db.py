from django.core.management.base import BaseCommand, CommandError
from product.models import ZCategory, ZProduct

# DIR_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(DIR_BASE)
# sys.path.append(DIR_BASE)
# from zopynfacts import products
from zopynfacts import products as source


class Command(BaseCommand):
    help = 'Initialize or alternately Update Product module database'

    def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):


        self.zfunct()

        for poll_id in options['poll_ids']:
            # try:
            #     poll = Poll.objects.get(pk=poll_id)
            # except Poll.DoesNotExist:
            #     raise CommandError('Poll "%s" does not exist' % poll_id)

            # poll.opened = False
            # poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully read poll "%s"' % poll_id))

    
    def zfunct(self):

        # Init db

        # Init category db

        ## Get Categories from db

        ## Get new categories 
        category_source_lst = source.download_categories('fr', 'fr')
        Ncat_src = len(category_source_lst)
        print('Categories count:', Ncat_src)

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

        print('Categories count:', len(category_source_lst))

        Nmax = 50
        Ncategory = len(category_lst)
        if Ncategory < Nmax:
            n = Nmax - Ncategory
            category_lst.extend(category_source_lst[:n])

        for idx, cat_dct in enumerate(category_lst):
            print(idx, 'Products:', cat_dct['products'], 'Name', cat_dct['name'])

        ### Get most complete/full categories
        ### Get randomly categories
        ## Add new categories into db 

        ## Update Categories into db (new and existing)

        # Update db
        # Get Product from category
        # Get existing product
        # Get healthiest and popular product


        # Get existing cat from 
        
        # nCategory = 50
        # delta = Ncat_src // nCategory
        # print('DELTA', delta)

        # cat_lst = [el_dct for idx, el_dct in enumerate(categories_dct['tags']) if idx % delta == 0]
        # for idx, cat_dct in enumerate(cat_lst):
        #     print(idx, cat_dct)
