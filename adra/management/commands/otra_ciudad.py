from django.core.management.base import BaseCommand, CommandError
from datetime import date
from adra.models import Persona, Alimentos,Hijo


class Command(BaseCommand):

    def handle(self, *args, **options):
        persona = Persona.objects.exclude(covid=True).filter(active=True)
        hijos = Hijo.objects.filter(active=True)
        print(persona.count())
        print(hijos.count())

