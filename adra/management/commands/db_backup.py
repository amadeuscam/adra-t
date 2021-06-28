import subprocess
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        username = settings.USER_DB
        password = settings.PASSWORD_DB
        database = settings.NAME_DB

        command_line = f"mysqldump -u {username} -p{password}  {database} > " \
                       f"{datetime.now().day}-{datetime.now().month}.sql"
        dc = subprocess.Popen(command_line, shell=True)
        dc.wait()
