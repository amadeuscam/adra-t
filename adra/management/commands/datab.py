from django.core.management.base import BaseCommand, CommandError
import  subprocess

class Command(BaseCommand):

    def handle(self, *args, **options):
        subprocess.Popen('mysqldump -h 0.0.0.0 -P 3306 -u -root masina | mysql -h 0.0.0.0 -P 3306 -u root masina',
                         shell=True)
