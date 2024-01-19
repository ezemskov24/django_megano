from datetime import datetime
import os

import celery
from django.conf import settings


class ImportLogger:
    def __init__(self, start, file_manager):
        self.log_messages = []
        self.start = start
        self.file_manager = file_manager

    def log(self, message):
        print(message)
        now = datetime.now()
        self.log_messages.append(f'[{now.time()}] {message}')

    def log_result(
        self,
        successful_imports=0,
        product_imports=0,
        successful_product_imports=0,
        image_imports=0,
        successful_image_imports=0,
        seller_product_imports=0,
        successful_seller_product_imports=0,
    ):
        message = f'Successfully imported {successful_imports} items: '
        details = []
        if product_imports:
            details.append(
                '{success}/{total} products'.format(
                    success=successful_product_imports,
                    total=product_imports,
                ),
            )
        if image_imports:
            details.append(
                '{success}/{total} product images'.format(
                    success=successful_image_imports,
                    total=image_imports,
                ),
            )
        if seller_product_imports:
            details.append(
                '{success}/{total} seller products'.format(
                    success=successful_seller_product_imports,
                    total=seller_product_imports,
                ),
            )
        message = message + ', '.join(details)

        self.log(message)

    def finalize_log(self):
        log = '\n'.join(self.log_messages)
        print(log)

        log_path = self.file_manager.get_log_path()
        self.file_manager.save_file(log, log_path)


class FileManager:
    def __init__(self, start):
        self.start = start
        self.filename = None

    @staticmethod
    def save_file(content, save_path):
        mode = 'wb' if isinstance(content, bytes) else 'w'

        with open(save_path, mode) as f:
            f.write(content)

    @staticmethod
    def remove_file(file_path):
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

    def get_log_path(self):
        logs_dir = settings.IMPORT_LOGS_DIR

        return self._get_file_path(logs_dir, 'log')

    def get_json_path(self, success):
        if success:
            target_dir = settings.IMPORT_SUCCESS_DIR
        else:
            target_dir = settings.IMPORT_FAILURE_DIR

        return self._get_file_path(target_dir, 'json')

    def _get_file_path(self, target_dir, file_extension):
        import_dir = settings.IMPORT_DIR
        if not os.path.exists(import_dir):
            os.mkdir(import_dir)

        if not os.path.exists(target_dir):
            os.mkdir(target_dir)

        today_dir = target_dir.joinpath(datetime.now().strftime('%Y-%m-%d'))
        if not os.path.exists(today_dir):
            os.mkdir(today_dir)

        filename = self._get_filename(file_extension)
        return today_dir.joinpath(filename)

    def _get_filename(self, extension=''):
        if not self.filename:
            self.filename = self.start.strftime(
                '%H:%M:%S - ',
            ) + celery.uuid()

        return self.filename + '.' + extension if extension else self.filename
