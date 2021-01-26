import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_analysis.settings')

app = Celery('stock_analysis')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_transport_options = {'visibility_timeout': 3600}  # 1 hour.
app.conf.broker_url = 'redis://127.0.0.1:6379/0'
app.conf.result_backend = 'redis://127.0.0.1:6379/0'
app.conf.task_serializer = 'json'

app.conf.imports = ['tasks.celery_jobs']

app.conf.update(
    task_routes = {
        'tasks.celery_jobs.*': {'queue': 'celery_jobs'},
    },
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
