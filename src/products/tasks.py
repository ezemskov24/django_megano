import json
import io
from os import path, PathLike
import shutil
from typing import Union, Dict
import zipfile

from celery import shared_task
from django.conf import settings
from django.core.files.images import ImageFile
from django.db import transaction
from django.utils.text import slugify

from products.models import Category, Product, Picture


@shared_task
def import_products(file: Union[str, PathLike[str], bytes]):
    original_path = None
    target_path = None
    filename = None
    if isinstance(file, PathLike) or isinstance(file, str):
        if path.exists(file) and path.isfile(file):
            original_path = file
            filename = path.basename(file)
    elif isinstance(file, bytes):
        file = io.BytesIO(file)
    else:
        return

    try:
        archive = zipfile.ZipFile(file)

        if archive.testzip():
            print('There are corrupted files in the archive')
            return

        file_names = _get_file_names_from_archive(archive)

        if not file_names.get('json'):
            print('There is no json file in the archive')
            raise FileNotFoundError('There is no json file in the archive')

        _add_products_from_archive_to_database(archive, file_names)

        if original_path and filename:
            success_dir = settings.IMPORT_SUCCESS_DIR
            target_path = success_dir.joinpath(filename)

    except Exception as e:
        print(f'{type(e)}: {e}')
        if original_path and filename:
            failure_dir = settings.IMPORT_FAILURE_DIR
            target_path = failure_dir.joinpath(filename)
    finally:
        if original_path and target_path:
            shutil.move(original_path, target_path)


def _get_file_names_from_archive(archive: zipfile.ZipFile):
    file_names = {}
    for info in archive.infolist():
        if not info.is_dir():
            if info.filename.endswith('.json'):
                if file_names.get('json'):
                    print('Too many json files')
                    return
                file_names['json'] = info.filename
            else:
                name_path = info.filename.split('/')
                if len(name_path) != 3:
                    continue
                file_names.setdefault(name_path[1], []).append(info.filename)
    print(file_names)

    return file_names


def _add_products_from_archive_to_database(
    archive: zipfile.ZipFile,
    file_names: Dict[str, str],
):
    products = json.loads(archive.read(file_names['json']))
    print(products)

    with transaction.atomic():
        for prod_name, prod_content in products.items():
            print(f'{prod_name} : {prod_content}')
            prod_content['category'] = Category.objects.filter(
                pk=prod_content['category'],
            ).first()
            if not prod_content.get('slug'):
                prod_content['slug'] = slugify(prod_content['name'])
            new_product = Product(**prod_content)
            new_product.save()

            prod_images = file_names.get(prod_name)
            for image_name in prod_images:
                name = path.basename(image_name)
                image = ImageFile(
                    io.BytesIO(archive.read(image_name)),
                    name=name,
                )
                new_image = Picture(
                    product=new_product,
                    image=image,
                )
                new_image.save()
            print(new_product)
