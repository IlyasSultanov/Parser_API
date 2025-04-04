from __future__ import absolute_import
import os
import logging
from celery import Celery

from P_parcer.settings import INSTALLED_APPS

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P_parcer.settings')

app = Celery('parser')

app.config_from_object('django.conf.settings', namespace='CELERY')

app.autodiscover_tasks(lambda: INSTALLED_APPS)