from __future__ import absolute_import
import os
import logging
from celery import Celery
from celery.schedules import crontab

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P_parcer.settings')

app = Celery('P_parcer')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'parse_categories': {
        'task': 'API.tasks.parse_categories',
        'schedule': crontab(hour=3, minute=0),
    },
}