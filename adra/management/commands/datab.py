from django.core.management.base import BaseCommand, CommandError
import  subprocess

class Command(BaseCommand):

    def handle(self, *args, **options):
        username = 'root'
        password = 'masina'
        database = 'adra_torrejon_new'

        with open('file.sql', 'w') as output:
            c = subprocess.Popen(['mysqldump', '-u', username, '-p%s' % password, database],
                                 stdout=output, shell=True)
