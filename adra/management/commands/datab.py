from django.core.management.base import BaseCommand, CommandError
import  subprocess

class Command(BaseCommand):

    def handle(self, *args, **options):
        subprocess.Popen('mysqldump  -u -root masina | mysql  -u root masina',
                         shell=True)
