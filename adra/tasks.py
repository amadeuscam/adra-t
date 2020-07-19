import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger


@periodic_task(
    run_every=(crontab(minute='1')),
    name="create_random_user_accounts",
    ignore_result=True
)
def create_random_user_accounts():
    for i in range(1, 12):
        print(i)
