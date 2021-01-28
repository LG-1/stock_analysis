import os
from celery.schedules import crontab

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
app.conf.timezone = 'Asia/Chongqing'

app.conf.imports = ['tasks.celery_jobs', 'tasks.update_holdernumber', 'tasks.update_stock_exchange']

app.conf.update(
    task_routes = {
        'tasks.celery_jobs.*': {'queue': 'celery_jobs'},
        'tasks.update_holdernumber.*': {'queue': 'celery_jobs'},
    },
)

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.celery_jobs.add',
        'schedule': 30.0,
        'args': (16, 16),
        'kwargs': {'test': 100}
    },
    'run-update-holder_job': {
        'task': 'tasks.update_holdernumber.all_holder_tasks',
        'schedule': crontab(hour=17, minute=59),
        'args': ()
    },
    'run-update_stock_job': {
        'task': 'tasks.update_stock_exchange.all_stock_tasks',
        'schedule': crontab(hour=18, minute=30),
        'args': (),
        'kwargs': {'days': 2}
    },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
