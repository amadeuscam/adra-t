from django.core.management.base import BaseCommand, CommandError
from adra.models import Persona

class Command(BaseCommand):


    def handle(self, *args, **options):
       persona = Persona.objects.all()[:50]
       for p in persona:
           p.domingo = 'Domingo 1'
           p.save()
        #SAVE
       persona2 = Persona.objects.all()[50:]
       for p2 in persona2:
           p2.domingo = 'Domingo 2'
           p2.save()