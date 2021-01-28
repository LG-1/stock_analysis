import tushare as ts
# ts.set_token('ad00beec7ad536862e87da4da49a6a95a1385973009fc949d16f1d94')


# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
