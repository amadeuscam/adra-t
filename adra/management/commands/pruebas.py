from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from adra.models import Persona,Hijo
from twilio.rest import Client


class Command(BaseCommand):

    def handle(self, *args, **options):

        total_familiares = Hijo.objects.all()
        total_per = Persona.objects.filter(active=False)
        print([t.numero_adra for t in total_per])

