import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoVlog.settings')

app = Celery('DjangoVlog')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.task_always_eager = getattr(settings, 'CELERY_TASK_ALWAYS_EAGER', False)