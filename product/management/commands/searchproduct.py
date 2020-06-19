import requests
from operator import itemgetter

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from product import views
from product.models import ZCategory, ZProduct

# DIR_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(DIR_BASE)
# sys.path.append(DIR_BASE)
# from zopynfacts import products
from zopynfacts import products as source


class Command(BaseCommand):
    help = 'Initialize or alternately Update Product module database'

    def add_arguments(self, parser):
        parser.add_argument('query', nargs='+', type=str)

    def handle(self, *args, **options):
        """Blablabla"""

        product_mdl = views.search_product(options['query'][0])

        if product_mdl:
            alternative_product_lst = views.get_alternative_product(product_mdl.code)
            for alternative_mdl in alternative_product_lst:
                product_mdl.alternatives.add(alternative_mdl)

        # Get all products sharing the same groups of the targeted product
