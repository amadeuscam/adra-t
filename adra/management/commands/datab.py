from django.core.management.base import BaseCommand, CommandError
import  subprocess
from datetime import datetime
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        username = settings.USER_DB
        password = settings.PASSWORD_DB
        database = settings.NAME_DB

        with open(f'{datetime.now().day}-{datetime.now().month}.sql', 'w') as output:
            c = subprocess.Popen(['mysqldump', '-u', username, '-p%s' % password, database],
                                 stdout=output, shell=True)
