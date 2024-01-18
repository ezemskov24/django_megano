import os
from datetime import datetime
import json
import io
from os import path, PathLike
import shutil
from typing import Union, Dict
import zipfile

import celery
from celery import shared_task
from django.conf import settings
from django.core.files.images import ImageFile
from django.db import transaction
from django.utils.text import slugify

from account.models import Seller
from products.models import Category, Product, Picture, SellerProduct


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
    log_messages = []
    start = datetime.now()
    try:
        log_messages.append(_get_formatted_message(f'Begin import'))
        archive = zipfile.ZipFile(file)

        if archive.testzip():
            print('There are corrupted files in the archive')
            raise ImportError('There are corrupted files in the archive')

        file_names = _get_file_names_from_archive(archive)

        if not file_names.get('json'):
            print('There is no json file in the archive')
            raise FileNotFoundError('There is no json file in the archive')

        _add_entries_from_archive_to_database(
            archive,
            file_names,
            log_messages,
        )

        log_messages.append(_get_formatted_message('Import finished'))

        if original_path and filename:
            success_dir = settings.IMPORT_SUCCESS_DIR
            target_path = success_dir.joinpath(filename)

    except Exception as e:
        print(f'Import failed due to {type(e).__name__}: {e}')
        log_messages.append(
            _get_formatted_message(
                f'Import failed due to {type(e).__name__}: {e}',
            ),
        )
        if original_path and filename:
            failure_dir = settings.IMPORT_FAILURE_DIR
            target_path = failure_dir.joinpath(filename)
    finally:
        if original_path and target_path:
            shutil.move(original_path, target_path)
        log = '\n'.join(log_messages)
        print(log)

        end = datetime.now()
        import_dir =  settings.IMPORT_DIR
        log_path = _get_log_path(start)
        with open(log_path, 'w') as f:
            f.write(log)


def _get_file_names_from_archive(archive: zipfile.ZipFile):
    file_names = {}
    for info in archive.infolist():
        if not info.is_dir():
            if info.filename.endswith('.json'):
                if file_names.get('json'):
                    print('Too many json files')
                    raise ImportError('Too many json files')
                file_names['json'] = info.filename
            else:
                name_path = info.filename.split('/')
                if len(name_path) != 3:
                    continue
                file_names.setdefault(name_path[1], []).append(info.filename)
    print(file_names)

    return file_names


def _add_entries_from_archive_to_database(
    archive: zipfile.ZipFile,
    file_names: Dict[str, str],
    log_messages,
):
    json_file = json.loads(archive.read(file_names['json']))
    products = json_file.get('products')
    seller_products = json_file.get('seller_products')

    with transaction.atomic():
        if products:
            new_products = _add_products_to_database(
                products,
                archive,
                file_names,
                log_messages
            )
        if seller_products:
            if new_products:
                _add_seller_products_to_database(
                    seller_products,
                    log_messages,
                    new_products,
                )
            else:
                _add_seller_products_to_database(seller_products, log_messages)


def _add_products_to_database(products, archive, file_names, log_messages):
    log_messages.append(_get_formatted_message(f'Importing products'))
    new_products = {}
    for prod_name, prod_content in products.items():
        try:
            print(f'{prod_name} : {prod_content}')
            prod_content['category'] = Category.objects.filter(
                pk=prod_content['category'],
            ).first()
            if not prod_content.get('slug'):
                prod_content['slug'] = slugify(prod_content['name'])
            new_product = Product(**prod_content)
            new_product.save()
            new_products[prod_name] = new_product

            prod_images = file_names.get(prod_name)
            if prod_images:
                _add_pictures_to_database(
                    prod_images,
                    new_product,
                    archive,
                    log_messages,
                )

            print(new_product)
            log_messages.append(
                _get_formatted_message(f'Product imported successfully'),
            )
        except Exception as e:
            print(f'Product import failed due to {type(e).__name__}: {e}')
            log_messages.append(
                _get_formatted_message(
                    f'Product import failed due to {type(e).__name__}: {e}'
                ),
            )
    if new_products:
        log_messages.append(
            _get_formatted_message(f'Imported {len(new_products)} products'),
        )
    return new_products


def _add_pictures_to_database(prod_images, product, archive, log_messages):
    log_messages.append(_get_formatted_message(f'Importing product images'))
    for image_name in prod_images:
        try:
            name = path.basename(image_name)
            image = ImageFile(
                io.BytesIO(archive.read(image_name)),
                name=name,
            )
            new_image = Picture(
                product=product,
                image=image,
            )
            new_image.save()
            log_messages.append(
                _get_formatted_message(f'Image imported successfully')
            )
        except Exception as e:
            print(f'Image import failed due to {type(e).__name__}: {e}')
            log_messages.append(
                _get_formatted_message(
                    f'Image import failed due to {type(e).__name__}: {e}',
                )
            )


def _add_seller_products_to_database(
        seller_products,
        log_messages,
        new_products={},
):
    log_messages.append(_get_formatted_message(f'Importing seller products'))
    count = 0
    for sell_prod in seller_products.values():
        try:
            sell_prod['seller'] = Seller.objects.filter(
                pk=sell_prod['seller'],
            ).first()
            if sell_prod.get('new'):
                sell_prod['product'] = new_products[str(sell_prod['product'])]
            else:
                sell_prod['product'] = Product.objects.filter(
                    pk=sell_prod['product'],
                ).first()

            if isinstance(sell_prod.get('new'), int):
                del sell_prod['new']

            new_seller_product = SellerProduct(**sell_prod)
            new_seller_product.save()
            count += 1
            log_messages.append(
                _get_formatted_message(f'SellerProduct imported successfully')
            )

        except Exception as e:
            print(f'SellerProduct import failed due to {type(e).__name__}: {e}')
            log_messages.append(
                _get_formatted_message(
                    f'SellerProduct import failed due to {type(e).__name__}: {e}'
                )
            )
    if count:
        log_messages.append(
            _get_formatted_message(f'Imported {len(new_products)} seller products'),
        )


def _get_formatted_message(message):
    now = datetime.now()
    return f'[{now.time()}] {message}'


def _get_log_path(start):
    logs_dir = settings.IMPORT_LOGS_DIR
    if not path.exists(logs_dir):
        os.mkdir(logs_dir)
    today_dir = logs_dir.joinpath(datetime.now().strftime('%Y-%m-%d'))
    if not path.exists(today_dir):
        os.mkdir(today_dir)
    log_name = start.strftime('%H:%M:%S - ') + celery.current_task.__name__ + '_' + celery.uuid() + '.log'
    return today_dir.joinpath(log_name)
