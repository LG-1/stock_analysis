

# Introduction

# Setting up
## django
    """ after setting up mysql connections"""
    python manage.py migrate

    python manage.py createsuperuser # liguang/gjingyun.li@163.com/


# Run
## task sample
    python -m tasks.update_holdernumber


# Test
## code test
    pytest unittests



## celery job test
    ### start up worker
    celery -A stock_analysis worker --loglevel=INFO -E --concurrency=1 -Q celery_jobs -P eventlet

        python .\manage.py shell
        from tasks.celery_jobs import add
        result = add.delay(4, 4)
        result.ready()

        add.apply_async((2, 2), queue='celery_jobs')

    celery -A stock_analysis beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler


## airflow test
not ready(2021-01-23), for airflow(2.0.0, ubuntu)
    airflow dags test example_bash_operator 2021-01-22