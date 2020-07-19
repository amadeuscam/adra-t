import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task
from celery import Celery
from celery.schedules import crontab

app = Celery()


@app.task
def create_random_user_accounts():
    for i in range(1, 12):
        print(i)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Ejecuta la tarea test('hello') cada 10 segundos
    sender.add_periodic_task(10.0, create_random_user_accounts, name='add every 10')

    # Ejecuta la tarea test('world') cada 10 segundos
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # # Ejecuta la tarea cada lunes a las 7:30 am
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )