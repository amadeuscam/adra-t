from django.core.management.base import BaseCommand, CommandError
import subprocess
from datetime import datetime
from pathlib import Path
import shutil
import time
import shlex
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        username = settings.USER_DB
        password = settings.PASSWORD_DB
        database = settings.NAME_DB

        command_line = f"mysqldump -u {username} -p{password}  {database} > {datetime.now().day}-{datetime.now().month}.sql"
        args = shlex.split(command_line)
        subprocess.Popen(args)
