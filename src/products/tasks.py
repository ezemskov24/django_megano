from os import PathLike
from typing import Union

from celery import shared_task

from .services.product_import.product_importer import ProductImporter


@shared_task
def import_products(file: Union[str, PathLike[str], bytes]):
    ProductImporter(file)
