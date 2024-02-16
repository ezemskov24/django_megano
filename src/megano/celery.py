import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'megano.settings')
app = Celery('megano', broker='amqp://guest:guest@rabbitmq:5672', backend='redis://redis:6379/1')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
