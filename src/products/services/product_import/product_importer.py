from datetime import datetime
import json
import io
from os import path, PathLike
from typing import Union
import zipfile

from django.core.files.images import ImageFile
from django.db import transaction
from django.utils.text import slugify

from .import_utils import ImportLogger, FileManager
from account.models import Seller
from products.models import Category, Product, Picture, SellerProduct


class ProductImporter:
    def __init__(self, file: Union[str, PathLike[str], bytes]):
        self.original_path = None
        self.target_path = None
        self.filename = None
        self.json = None
        self.start = datetime.now()
        self.file_manager = FileManager(self.start)
        self.logger = ImportLogger(self.start, self.file_manager)
        self.product_imports = 0
        self.successful_product_imports = 0
        self.image_imports = 0
        self.successful_image_imports = 0
        self.seller_product_imports = 0
        self.successful_seller_product_imports = 0

        self._import_products(file)

    def _import_products(self, file: Union[str, PathLike[str], bytes]):
        try:
            self.logger.log(f'Begin product_import')
            self._check_file(file)
            self._check_archive()
            self._add_entries_from_archive_to_database()
            self.logger.log('Import finished')

            self.successful_imports = sum(
                (
                    self.successful_product_imports,
                    self.successful_product_imports,
                    self.successful_seller_product_imports,
                )
            )
            if self.successful_imports:
                self.logger.log_result(
                    self.successful_imports,
                    self.product_imports,
                    self.successful_product_imports,
                    self.image_imports,
                    self.successful_image_imports,
                    self.seller_product_imports,
                    self.successful_seller_product_imports,
                )
        except Exception as e:
            self.logger.log(f'Import failed due to {type(e).__name__}: {e}')
            self.successful_imports = 0
        finally:
            self.logger.finalize_log()
            success = self.successful_imports > 0
            if self.json:
                file_path = self.file_manager.get_json_path(success)
                file = self.archive.read(self.json)
                self.file_manager.save_file(file, file_path)
            if self.original_path:
                self.file_manager.remove_file(self.original_path)

    def _check_file(self, file: Union[str, PathLike[str], bytes]):
        if isinstance(file, PathLike) or isinstance(file, str):
            if path.exists(file) and path.isfile(file):
                self.file = file
                self.original_path = file
        elif isinstance(file, bytes):
            self.file = io.BytesIO(file)
        else:
            raise ValueError('Not a viable file provided')

    def _check_archive(self):
        self.archive = zipfile.ZipFile(self.file)

        if self.archive.testzip():
            raise ImportError('There are corrupted files in the archive')

        self._get_file_names_from_archive()

        self.json = self.file_names.get('json')
        if not self.json:
            raise FileNotFoundError('There is no json file in the archive')

    def _get_file_names_from_archive(self):
        self.file_names = {}
        for info in self.archive.infolist():
            if not info.is_dir():
                if info.filename.endswith('.json'):
                    if self.file_names.get('json'):
                        print('Too many json files')
                        raise ImportError('Too many json files')
                    self.file_names['json'] = info.filename
                else:
                    name_path = info.filename.split('/')
                    if len(name_path) != 3:
                        continue
                    self.file_names.setdefault(name_path[1], []).append(
                        info.filename,
                    )
        print(self.file_names)

    def _add_entries_from_archive_to_database(self):
        json_file = json.loads(self.archive.read(self.json))
        self.products = json_file.get('products')
        self.seller_products = json_file.get('seller_products')

        with transaction.atomic():
            if self.products:
                self._add_products_to_database()
            if self.seller_products:
                self._add_seller_products_to_database()

    def _add_products_to_database(self):
        self.logger.log(f'Importing products')
        self.new_products = {}

        for prod_name, prod_content in self.products.items():
            self.add_product_to_database(prod_content, prod_name)

        if self.successful_product_imports:
            self.logger.log(f'Imported {self.successful_product_imports} products')

    def add_product_to_database(self, prod_content, prod_name):
        self.product_imports += 1
        try:
            with transaction.atomic():
                prod_content['category'] = Category.objects.filter(
                    pk=prod_content['category'],
                ).first()
                if not prod_content.get('slug'):
                    prod_content['slug'] = slugify(prod_content['name'])
                new_product = Product(**prod_content)
                new_product.save()
                self.successful_product_imports += 1
                self.new_products[prod_name] = new_product

                prod_images = self.file_names.get(prod_name)
                if prod_images:
                    self._add_pictures_to_database(
                        prod_images,
                        new_product
                    )
                self.logger.log(f'Product imported successfully')
        except Exception as e:
            self.logger.log(
                f'Product product_import failed due to {type(e).__name__}: {e}'
            )

    def _add_pictures_to_database(
        self,
        prod_images,
        product
    ):
        self.logger.log(f'Importing product images')
        for image_name in prod_images:
            self.image_imports += 1
            try:
                with transaction.atomic():
                    name = path.basename(image_name)
                    image = ImageFile(
                        io.BytesIO(self.archive.read(image_name)),
                        name=name,
                    )
                    new_image = Picture(
                        product=product,
                        image=image,
                    )
                    new_image.save()
                    self.successful_image_imports += 1
                    self.logger.log(f'Image imported successfully')
            except Exception as e:
                self.logger.log(
                    f'Image product_import failed due to {type(e).__name__}: {e}'
                )

    def _add_seller_products_to_database(self):
        self.logger.log(f'Importing seller products')

        for sell_prod in self.seller_products.values():
            self._add_seller_product_to_database(sell_prod)
        if self.successful_seller_product_imports:
            self.logger.log(
                f'Imported {self.successful_seller_product_imports} seller products'
            )

    def _add_seller_product_to_database(self, sell_prod):
        self.seller_product_imports += 1
        try:
            with transaction.atomic():
                self._process_seller_product_params(sell_prod)
                new_seller_product = SellerProduct(**sell_prod)
                new_seller_product.save()
                self.successful_seller_product_imports += 1
                self.logger.log(f'SellerProduct imported successfully')
        except Exception as e:
            self.logger.log(
                f'SellerProduct product_import failed due to {type(e).__name__}: {e}',
            )

    def _process_seller_product_params(self, sell_prod):
        sell_prod['seller'] = Seller.objects.filter(
            pk=sell_prod['seller'],
        ).first()
        if sell_prod.get('new'):
            sell_prod['product'] = self.new_products[
                str(sell_prod['product'])]
        else:
            sell_prod['product'] = Product.objects.filter(
                pk=sell_prod['product'],
            ).first()

        if isinstance(sell_prod.get('new'), int):
            del sell_prod['new']