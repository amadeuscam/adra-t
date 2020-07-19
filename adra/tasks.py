import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from datetime import timedelta
from celery.task import PeriodicTask


class ProcessClicksTask(PeriodicTask):
    run_every = timedelta(seconds=30)

    def run(self, **kwargs):
        print("HELLO celery")
