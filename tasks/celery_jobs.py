from celery import shared_task

@shared_task
def add(x, y, *args, **kwargs):
    print(x + y + kwargs.get('test', 10))
    return print(x + y + kwargs.get('test', 10))
