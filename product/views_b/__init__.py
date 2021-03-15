import os, sys
import json

import logging


from django.conf import settings as project_settings
from django.shortcuts import render


# DIR_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(DIR_BASE)
# sys.path.append(DIR_BASE)

from ..models import ZProduct, ZCategory, ZSearch, ZCategory_Product

sys.path.append(project_settings.BASE_DIR)
from zopynfacts import products

from zopynfacts import products



# Get an instance of a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def print_product_list(zlist):
    for idx, product_db in enumerate(zlist):
        print(idx, '-', product_db.brands, '-', product_db.name, '-', product_db.unique_scans_n)
