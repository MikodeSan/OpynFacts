import os, sys

import logging


from django.conf import settings as project_settings
from django.shortcuts import render


sys.path.append(project_settings.BASE_DIR)
sys.path.append(project_settings.PROJECT_DIR)
sys.path.append(os.path.join(project_settings.BASE_DIR, "product"))

from product.models import ZProduct, ZCategory, ZSearch, ZCategory_Product

from zopynfacts import products


# Get an instance of a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def print_product_list(zlist):
    for idx, product_db in enumerate(zlist):
        print(
            idx,
            "-",
            product_db.brands,
            "-",
            product_db.name,
            "-",
            product_db.unique_scans_n,
        )
