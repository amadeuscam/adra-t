import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task


@shared_task
def create_random_user_accounts():
    for i in range(1, 12):
        print(i)
